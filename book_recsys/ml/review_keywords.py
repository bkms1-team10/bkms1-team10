import warnings
warnings.filterwarnings('ignore')

import os
import sys
sys.path.append('../')

from collections import defaultdict
import re
from tqdm import tqdm
import pandas as pd

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from ml.config import *
from ml.query import *
from ml.utils import *

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


def main():
    
    # db connect
    db_path = os.path.join(WORKING_DIRECTORY, 'resources/project.db')
    con = connection(db_path)

    print('Loading dataset...')
    ratings = read_table(con, ratings_query)
    reviews = read_table(con, reviews_query)

    review_df = pd.merge(ratings, reviews, on='review_id', how = 'inner')
    review_df = review_df[['book_id', 'review_text']]
    
    review_df['review_text'] = review_df['review_text'].fillna('')
    
    # # 테스트로 100개 행만 (전체 행으로 실행하는 경우 1시간 20분 정도 걸림)
    # review_df = review_df.head(100)
    
    review_df['review_text'] = review_df['review_text'].apply(clean_text)

    reviews_new = review_df.groupby('book_id')['review_text'].apply(list).to_dict()
    book_list = list(reviews_new.keys())
    review_keywords = defaultdict(list)

    print('Extracting review keywords...')
    for i in tqdm(book_list):
        corpus = reviews_new[i]
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)

        try:
            vecs = vectorizer.fit_transform(corpus)
            feature_names = vectorizer.get_feature_names()  # 에러나는 경우 get_feature_names_out()로 시도
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
    
    print('Saving results...')
    keyword_df.to_csv(os.path.join(WORKING_DIRECTORY, 'results/review_keywords.csv'), index=False)

    print('Done')


if __name__ == "__main__":

    main()