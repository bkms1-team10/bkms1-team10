from flask import session ,jsonify  , request
from server import app ,db
from models.user import Books 
from schemas.user import BooksSchema
from sqlalchemy import func, desc



@app.route('/get_books/', methods=['GET'])
def get_books():
    """
    메인 / 인덱스 페이지 에서 책들 평균 별점 높은것 가져오는 함수
    실제 DB Books 에서는 평균 점수 컬럼이 있다 이것으로 보면 될지   / 1번 간단하게 가능
    아니면 실제 이 웹사이트에서 사용자들이 남긴 평점으로 해야 하는것인지  /  2번 DB 구조 전체 변경 필요
    아니면 레이팅 테이블에서 연동되어 있는 books id와 그룹핑을 맺어 계산 해야 하는것인지 알수없음  / 3번 그룹화 필요

    3번 쿼리
    SELECT rating, book_id, avg(rating) AS avg_rate FROM Ratings GROUP BY book_id order by avg_rate desc

    지금 평균 점수 높은곳 100개로 작성 (1번 로직)
    26번째 줄 100 변경하면 숫자 변경 가능
    
    """
    books_query = db.session.query(Books).order_by(Books.average_rating.desc())
    books_data = BooksSchema().dump(books_query.limit(100), many=True)


    return jsonify(books_data = books_data)

        



@app.route('/search_book/', methods=['POST'])
def search_book():

    data = request.form

    title = data['title']


    book_data = db.session.query(Books).filter(Books.title.like("%"+title+"%")).all()
    book_data = BooksSchema().dump(book_data, many=True)


    return jsonify(books_data = book_data)

        
