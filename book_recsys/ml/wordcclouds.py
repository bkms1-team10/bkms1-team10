import argparse
from collections import defaultdict
import re
from tqdm import tqdm

import numpy as np
import pandas as pd

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

from ml.utils import *

import warnings
warnings.filterwarnings('ignore')

os.environ["NCCL_DEBUG"] = "INFO"

# 불용어 목록 다운로드
nltk.download('stopwords')

# 불용어 목록 가져오기
stopwords = set(stopwords.words('english'))


def clean_text(x):
    x = re.sub(r'\d', ' ', x)
    x = re.sub("\n"," ",x)
    x = re.sub("<.*?>"," ",x)
    x = re.sub("\s+", " ", x).strip()
    x = re.sub(r'\b\w*read\w*\b', ' ', x)
    x = re.sub(r'\b\w*book\w*\b', ' ', x)
    return x


def main(args):

    wordcloud_dir_path = os.path.join(os.environ['WORKING_DIRECTORY'], args.wordcloud_dir)
    os.makedirs(wordcloud_dir_path, exist_ok=True)

    log_info('Load review dataset...')
    dataset_dir_path = os.path.join(os.environ['WORKING_DIRECTORY'], args.dataset_dir)
    curr_date = seconds_to_timestring(get_current_time_seconds(), '%Y-%m-%d')
    dataset_date_path = os.path.join(dataset_dir_path, 'stnd_ymd={0}'.format(curr_date))
    review_df = pd.read_csv(os.path.join(dataset_date_path, 'reviews.csv'), usecols=['book_id', 'review_text'])
    review_df['review_text'] = review_df['review_text'].fillna('')
    review_df = review_df.head(1000)  # 테스트로 1000개 행만 (전체 행으로 실행하는 경우 1시간 20분 정도 걸림)

    log_info('Preprocessing review text...')
    review_df['review_text'] = review_df['review_text'].apply(clean_text)

    reviews_new = review_df.groupby('book_id')['review_text'].apply(list).to_dict()
    book_list = list(reviews_new.keys())
    review_keywords = defaultdict(list)

    log_info('Extracting review keywords...')
    for i in tqdm(book_list):
        corpus = reviews_new[i]
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)

        try:
            vecs = vectorizer.fit_transform(corpus)
            feature_names = vectorizer.get_feature_names_out()
            dense = vecs.todense()
            lst1 = dense.tolist()
            tfidf_matrix = pd.DataFrame(lst1, columns=feature_names)
            keywords = tfidf_matrix.T.sum(axis=1).sort_values(ascending=False).index[:10].tolist()
            review_keywords[i].append(keywords)

        except ValueError:
            pass

    keyword_df = pd.DataFrame.from_dict(review_keywords, orient='index', columns=['keywords'])
    keyword_df.reset_index(inplace=True)
    keyword_df.columns = ['book_id', 'keywords']
    log_info('Saving results...')
    keyword_df.to_csv(os.path.join(wordcloud_dir_path, 'review_keywords.csv'), index=False)

    log_info('Done')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset_dir', default='resources/datasets', type=str)
    parser.add_argument('--wordcloud_dir', default='results/wordcloud', type=str)

    args = parser.parse_args()

    init_logger()

    main(args)