import sqlite3
from sqlite3 import Error
import pandas as pd


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