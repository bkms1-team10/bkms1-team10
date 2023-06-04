from flask import Flask, render_template, redirect, url_for, session, request 
import os
from flask_sqlalchemy import SQLAlchemy
import base


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Daniel Hanjoo Rhee/Documents/Downloads/BKMS0604/project.db/project.db'
base.db = SQLAlchemy(app)


from models.user import Books ,Users
from schemas.user import BooksSchema
from flask import session, render_template ,request , redirect , url_for , current_app , jsonify



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

        


@app.route('/login', methods=['GET', 'POST'])
def login():     
    ## 세션 정보 있으면 home로 이동


    if request.method == 'POST':
        data = request.form

        id = data['id']
        pw = data['pw']
        base.db.session.query(Users).order_by(Users.id.desc())
        user = Users.query.filter(Users.user_id == id).first()

        if user is None:
            current_app.logger.info('%s, / : none id' % (id))
            return 'ID_NOT_FOUND'
        
        if user.pw != pw :
            current_app.logger.info('%s, / : PASSWORD_NOT_FOUND ' % (id))
            return 'PASSWORD_NOT_FOUND'


        session["userID"] = id



        ##로그인 정보 일치하는 지 확인
        ##1) 아이디 검색
        ##2) 아이디+비밀번호 검색
        ##1) 2) 결과 없으면 html 출력 시 parameter로 message 전달 ID_NOT_FOUND / PASSWORD_NOT_FOUND, header = 'login'
        
        ###############################
        #message='ID_NOT_FOUND'       
        #message='PASSWORD_NOT_FOUND'
        #return render_template("/login/login.html", status='login', message=message)
        ################################        
        
        ##2) 결과 있으면 세션 설정(하단 코드)

        current_app.logger.info("로그인 성공")
        return "success"
    else:
        header='login'
        return render_template("/login/login.html", status=header)


@app.route('/register', methods=["POST"])
def register():
    """
    회원가입
    상세 주소 구 동 제외 했습니다.
    """


    data = request.form

    test_query = base.db.session.query(Users).order_by(Users.id.desc())
    test_query =test_query.first()


    users = {}
    users['id'] = int(test_query.id) + 1
    users['user_id'] = data['userid']
    users['pw'] = data['password']
    users['nickname'] = data['username']
    users['email'] = data['email']
    # users['postcode'] = data['postcode']
    users['address'] = data['address']
    users['address_dong'] = ""
    users['lat_long'] = ""
    users['lat'] = ""
    users['address_gu'] = ""
    users['long'] = ""
    # user = Users(nickname = data['username'], email = data['email'], pw= data['password'], address = data['address'] )

                            
    user = Users(** users)
    base.db.session.add(user)
    base.db.session.commit()


    return 'true'


@app.route('/idCheck/', methods=['POST'])
def idCheck():
    data = request.form['userID']
    code = "0"
    ## 1)data(유저가 입력한 아이디) 중복인지 확인
    ## 2)중복이면 code = "1"
    return code


@app.route('/index/')
def landing():
    ## 세션 정보 있으면 home로 이동, 없으면 landing page 출력
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

@app.route('/map/')
def map():
    return render_template("/bookInfo/map.html")



from flask import session 
from models.user import Books 
from schemas.user import BooksSchema

@app.route('/logout/')
def logout():
    session.pop('userID', None)
    return redirect(url_for('landing'))

@app.route('/join/')
def join():
    ## 세션 정보 있으면 home로 이동
    if 'userID' in  session:
        return redirect(url_for('home'))
    else:
        header='login'
        return render_template("/login/join.html", status=header)    

@app.route('/')
def home():

    if 'userID'  in  session:
        header='logout'
        return render_template("/home/home.html", status=header)
    else:
        return redirect(url_for('landing'))
    

@app.route('/login_view')
def login_view():
    if 'userID'  in  session:

        return redirect(url_for('landing'))
    return render_template("/login/login.html")



@app.route('/search/')
def search():
    if 'userID' in session:
        header='logout'
        return render_template("/search/search.html", status=header)
    else:
        return redirect(url_for('landing'))
    


@app.route('/bookInfo/<int:id>')
def bookInfo(id):
    """
    북 id 값 파라미터로 받고 해당 책 상세 내용 불러서 프론트에 던지기
    """

    if 'userID'not in session:
        return redirect(url_for('landing'))
    
    else:

        book_data = base.db.session.query(Books).filter(Books.book_id == id).first()
        return render_template("/bookinfo/bookinfo.html", book = book_data)
    


app.debug = True
app.run('127.0.0.1', port=5500)