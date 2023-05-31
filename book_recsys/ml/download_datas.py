import argparse
import pandas as pd
import sqlite3
from sqlite3 import Error

from ml.utils import *
from ml.query import *


def connection(file_name):
    try:
        con = sqlite3.connect(file_name)  # db 연결
        return con
    except Error:
        print(Error)


def read_table(con, query):
    cursor = con.cursor()
    cursor.execute(query)  # 쿼리 실행
    rows = cursor.fetchall()  # 모든 행 읽어오기
    cols = [column[0] for column in cursor.description]  # 필드 이름 가져오기
    df = pd.DataFrame.from_records(data=rows, columns=cols)  # pd dataframe으로 만들기
    return df


def main(args):

    log_info('Start data extracting process...')

    dataset_dir_path = os.path.join(os.environ['WORKING_DIRECTORY'], args.dataset_dir)
    curr_date = seconds_to_timestring(get_current_time_seconds(), '%Y-%m-%d')
    dataset_date_path = os.path.join(dataset_dir_path, 'stnd_ymd={0}'.format(curr_date))
    os.makedirs(dataset_date_path, exist_ok=True)

    log_info('Connectiong DB...')
    db_path = os.path.join(os.environ['WORKING_DIRECTORY'], args.db_file_name)
    con = connection(db_path)

    log_info('Reading tables...')
    query_list = [authors_query, books_query, reviews_query, users_query]
    csv_list = ['authors', 'books', 'reviews', 'users']
    for idx, query in enumerate(query_list):
        df = read_table(con, query)
        log_info(f'Saving {csv_list[idx]}.csv...')
        df.to_csv(os.path.join(dataset_date_path, '{0}.csv'.format(csv_list[idx])), index=False)

    log_info('Data download task is done')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_dir', default='resources/datasets', type=str)
    parser.add_argument('--db_file_name', default='resources/project.db', type=str)
    args = parser.parse_args()

    init_logger()

    main(args)