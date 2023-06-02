import argparse
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds
from sklearn.feature_extraction.text import TfidfVectorizer  # tf-idf
from sklearn.decomposition import LatentDirichletAllocation  # LDA

from ml.utils import *

import warnings
warnings.filterwarnings('ignore')

os.environ["NCCL_DEBUG"] = "INFO"


def recommend_books(df_svd_preds, user_idx, ori_books_df, ori_ratings_df, num_recommendations, default):
    if user_idx != 0:

        # 현재는 index로 적용이 되어있으므로 user_idx - 1을 해야함
        user_row_number = user_idx - 1

        # 최종적으로 만든 pred_df에서 사용자 index에 따라 책 데이터 정렬 -> 책 평점이 높은 순으로 정렬
        sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)

        # 원본 평점 데이터에서 user id에 해당하는 데이터를 뽑기
        user_data = ori_ratings_df[ori_ratings_df.user_idx == user_idx]

        # 위에서 뽑은 user_data와 원본 책 데이터를 합치기
        user_history = user_data.merge(ori_books_df, on='book_id').sort_values(['rating'], ascending=False)

        # 원본 책 데이터에서 유저가 읽은 책 데이터를 제외한 데이터를 추출
        recommendations = ori_books_df[~ori_books_df['book_id'].isin(user_history['book_id'])]

        # 유저의 평점이 높은 순으로 정렬된 데이터와 위 recommendations을 합치기
        recommendations = recommendations.merge(pd.DataFrame(sorted_user_predictions).reset_index(), on='book_id')
        recommendations = recommendations.rename(columns={user_row_number: 'Predictions'}).sort_values('Predictions',
                                                                                                       ascending=False).iloc[
                          :num_recommendations, :]
        recommendations = recommendations[['book_id', 'description']].set_index('book_id')['description'].to_dict()

    else:
        recommendations = default

    return recommendations


def get_topics(components, feature_names, n=15):
    result = {}
    for idx, topic in enumerate(components):
        topic_terms = [(feature_names[i]) for i in topic.argsort()[:-n - 1:-1]]
        result[idx] = topic_terms
    return result


def clustering_books(vectorizer, num_labels, book_rcmm):

    X = vectorizer.fit_transform(list(book_rcmm.values()))

    lda_model = LatentDirichletAllocation(n_components=num_labels, learning_method='online', random_state=777,
                                          max_iter=1)
    lda_top = lda_model.fit_transform(X)

    terms = vectorizer.get_feature_names_out()  # 단어 집합. 1,000개의 단어가 저장됨.
    keywords = get_topics(lda_model.components_, terms)

    result_dict = {}
    labels = np.argmax(lda_top, axis=1)
    book_ids = np.array(list(book_rcmm.keys()))

    for l, b in zip(labels, book_ids):
        if l not in result_dict:
            result_dict[l] = []
        result_dict[l].append(b)

    result_dict = dict(sorted(result_dict.items(), key=lambda x: x[0]))

    return result_dict, keywords


def main(args):

    book_rcmm_dir_path = os.path.join(os.environ['WORKING_DIRECTORY'], args.book_rcmm_dir)
    os.makedirs(book_rcmm_dir_path, exist_ok=True)

    dataset_dir_path = os.path.join(os.environ['WORKING_DIRECTORY'], args.dataset_dir)
    curr_date = seconds_to_timestring(get_current_time_seconds(), '%Y-%m-%d')
    dataset_date_path = os.path.join(dataset_dir_path, 'stnd_ymd={0}'.format(curr_date))

    log_info('Load datasets...')
    books_df = pd.read_csv(os.path.join(dataset_date_path, 'books.csv'),
                           usecols=['book_id', 'description', 'average_rating'])
    reviews_df = pd.read_csv(os.path.join(dataset_date_path, 'reviews.csv'),
                             usecols=['user_id', 'book_id', 'rating'])
    users_df = pd.read_csv(os.path.join(dataset_date_path, 'users.csv'), usecols=['user_id'])

    # 읽은 횟수가 10보다 적은 책은 삭제
    log_info('Preprocessing...')
    counts = reviews_df['book_id'].value_counts()
    valid_book_ids = counts[counts >= args.min_book_logs_cnt].index
    reviews_df = reviews_df[reviews_df['book_id'].isin(valid_book_ids)]

    # 인덱스로 매핑된 user_id 열 추가
    user_mapping = {user_id: idx + 1 for idx, user_id in enumerate(reviews_df['user_id'].unique())}

    reviews_df['user_idx'] = reviews_df['user_id'].map(user_mapping)
    reviews_df['user_idx'] = reviews_df['user_idx'].astype(int)

    users_df['user_idx'] = users_df['user_id'].map(user_mapping)
    users_df['user_idx'] = users_df['user_idx'].fillna(0)
    users_df['user_idx'] = users_df['user_idx'].astype(int)
    users_df = users_df.head(100)  # 테스트로 100개 행만

    # 이력 없는 유저들에게는 평점이 4보다 크면서 이력 개수가 많은 책들을 추천
    default = books_df[books_df['average_rating'] > 4.0]
    log_cnt = reviews_df['book_id'].value_counts()
    log_cnt = pd.DataFrame({'book_id': list(log_cnt.keys()), 'cnt': list(log_cnt.values)})
    default = pd.merge(default, log_cnt, on='book_id').sort_values('cnt', ascending=False).iloc[:args.num_recommendations, :]
    default = default[['book_id', 'description']].set_index('book_id')['description'].to_dict()

    # 각 유저를 행으로, 각 책을 열로하는 피폿테이블 생성
    log_info('Reviews_df to pivot...')
    df_user_book_ratings = reviews_df.pivot(
        index='user_id',
        columns='book_id',
        values='rating'
    ).fillna(0)

    matrix = df_user_book_ratings.values  # pivot_table 값을 numpy matrix로 만든 것
    user_ratings_mean = np.mean(matrix, axis=1)  # 사용자의 평균 평점
    matrix_user_mean = matrix - user_ratings_mean.reshape(-1, 1)  # 유저-책에 대해 사용자 평균 평점을 뺀 것

    log_info('Running book recsys...')
    # scipy에서 제공해주는 svd
    # U 행렬, sigma 행렬, V 전치 행렬을 반환.
    U, sigma, Vt = svds(matrix_user_mean, k=12)
    sigma = np.diag(sigma)

    # U, Sigma, Vt의 내적을 수행하면, 다시 원본 행렬로 복원됨 + 사용자 평균 rating을 적용
    svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns=df_user_book_ratings.columns)

    # 추천
    users_df['book_rcmm'] = users_df.apply(lambda x: recommend_books(df_svd_preds, x['user_idx'], books_df, reviews_df,
                                                                     args.num_recommendations, default), axis=1)

    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)  # 상위 1,000개의 단어를 보존
    users_df[['book_ids', 'keywords']] = users_df.apply(lambda x: clustering_books(vectorizer, args.num_labels, x['book_rcmm']),
                                                        axis=1, result_type="expand")
    users_df = users_df.drop(columns=['book_rcmm', 'user_idx'])
    log_info('Saving results...')
    users_df.to_csv(os.path.join(book_rcmm_dir_path, 'book_rcmm_result.csv'), index=False)

    log_info('Done')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_dir', default='resources/datasets', type=str)
    parser.add_argument('--book_rcmm_dir', default='results/book_rcmm', type=str)
    parser.add_argument('--min_book_logs_cnt', default=10, type=int)
    parser.add_argument('--num_recommendations', default=25, type=int)
    parser.add_argument('--num_labels', default=5, type=int)

    args = parser.parse_args()

    init_logger()

    main(args)