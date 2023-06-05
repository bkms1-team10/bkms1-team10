from flask import Flask, render_template, redirect, url_for, session, request 
import os
from flask_sqlalchemy import SQLAlchemy
import base


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\project.db'
base.db = SQLAlchemy(app)


from models.user import Books ,Users
from schemas.user import BooksSchema
from flask import current_app , jsonify



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
    books_query = base.db.session.query(Books).order_by(Books.average_rating.desc())
    books_data = BooksSchema().dump(books_query.limit(100), many=True)
    return jsonify(books_data = books_data)




@app.route('/search_book/', methods=['POST'])
def search_book():
    """
    책 검색창 
    """
    data = request.form

    title = data['title']


    book_data = base.db.session.query(Books).filter(Books.title.like("%"+title+"%")).all()
    book_data = BooksSchema().dump(book_data, many=True)


    return jsonify(books_data = book_data)


@app.route('/login/', methods=['GET', 'POST'])
def login():     
    ## 세션 정보 있으면 home로 이동
    if 'userID' in session:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            data = request.form

            id = data['id']
            pw = data['pw']
            base.db.session.query(Users).order_by(Users.id.desc())
            user = Users.query.filter(Users.user_id == id).first()
            
            """
            ##로그인 정보 일치하는 지 확인
            ##1) 아이디 검색
            if user is None:
                current_app.logger.info('%s, / : none id' % (id))
                return 'ID_NOT_FOUND'
            
            ##2) 아이디+비밀번호 검색
            if user.pw != pw :
                current_app.logger.info('%s, / : PASSWORD_NOT_FOUND ' % (id))
                return 'PASSWORD_NOT_FOUND'
            """
            session["userID"] = id
            current_app.logger.info("로그인 성공")
            return "success"
        else:
            header='login'
            return render_template("/login/login.html", status=header)


@app.route('/logout/')
def logout():
    session.pop('userID', None)
    return redirect(url_for('landing'))    


@app.route('/join/', methods=['GET', 'POST'])
def join():
    if 'userID' in session:
        return redirect(url_for('home'))
    else:
        if request.method == 'GET' :
            header='login'
            return render_template("/login/join.html", status=header)
        elif request.method == 'POST':
            ##회원가입 form에서 데이터 받아서 db에 저장
            ##id 중복 검사 및 비밀번호, 이메일 유효성 검사는 이전에 완료했으므로 insert만 하면 됨
            
            """
            회원가입
            상세 주소 구 동 제외 했습니다.
            """
            userID = request.form['userID']
            password = request.form['password']
            username = request.form['username']
            email = request.form['email']
            lat = request.form['lat']
            long = request.form['long']

            test_query = base.db.session.query(Users).order_by(Users.id.desc())
            test_query =test_query.first()
            
            users = {}
            users['id'] = int(test_query.id) + 1
            users['user_id'] = request.form['userID']
            users['pw'] = request.form['password']
            users['nickname'] = request.form['username']
            users['email'] = request.form['email']
            users['lat'] = request.form['lat']
            users['long'] = request.form['long']

            user = Users(** users)
            base.db.session.add(user)
            base.db.session.commit()
            print(userID, password, username, email, lat, long)
            return redirect(url_for('login'))


@app.route('/idCheck/', methods=['POST'])
def idCheck():
    data = request.form['userID']
    code = "0"
    ## 1)data(유저가 입력한 아이디) 중복인지 확인
    ## 2)중복이면 code = "1"
    return code


@app.route('/index/')
def landing():
    if 'userID' in session:
        return redirect(url_for('home'))
    else:
        return render_template("index.html")



@app.route('/share/')
def share():
    if 'userID' in session:
        header='logout'
        return render_template("/share/share.html", status=header)
    else:
        return redirect(url_for('landing')) 


from models.user import Books 
from schemas.user import BooksSchema

@app.route('/')
def home():
    if 'userID'  in  session:
        header='logout'
        
        seriesList = {}
        title1 = "평균 별점이 높은 책"
        seriesList[title1] = base.db.session.query(Books).order_by(Books.average_rating.desc()).limit(100)       
        
        title2 = "취미"
        seriesList[title2] = base.db.session.query(Books).order_by(Books.average_rating.desc()).limit(100)
        return render_template("/home/home.html", status=header, seriesList=seriesList)

    else:
        return redirect(url_for('landing'))
    
@app.route('/bookInfo/<int:id>')
def book_info(id):
    if 'userID' in session:
        header='logout'
        print(session["userID"])
        # 해당 책의 ID를 이용하여 책 상세 정보를 가져온다.
        book = base.db.session.query(Books).filter(Books.book_id == id).first()
        if book:
            ## 유저 위치 정보(북 쉐어 찾을 때 지도 중심 설정)
            userLoc = ["37.553091", "126.845341"]

            ## 북 쉐어 리스트
            bookShareList = []
            user1 = {}
            user1['nickname'] = "닉네임1"
            user1['email'] = "aaa@bbb.ccc"
            user1['lat']="37.5537"
            user1['long']="126.840"
            bookShareList.append(user1)

            user2 = {}
            user2['nickname'] = "닉네임2"
            user2['email'] = "ddd@eee.ffff"
            user2['lat']="37.5535"
            user2['long']="126.842"
            bookShareList.append(user2)
            return render_template("/bookinfo/bookinfo.html", status=header, book=book, userLoc = userLoc, bookShareList=bookShareList)
        else:
            return render_template("/error/404.html")
    else:
        return redirect(url_for('landing'))

@app.route('/search/')
def search():
    if 'userID' in session:
        header='logout'
        return render_template("/search/search.html", status=header)
    else:
        return redirect(url_for('landing'))
    


app.debug = True
app.run('127.0.0.1', port=5500)