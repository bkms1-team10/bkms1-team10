from flask import Flask, render_template, redirect, url_for, session, request 
import os
from flask_sqlalchemy import SQLAlchemy
import base
from haversine import haversine

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\project.db'
base.db = SQLAlchemy(app)


from models.user import Books ,Users, Ratings, Reviews, Authors, Sharings
from schemas.user import BooksSchema
from flask import current_app , jsonify


@app.route('/index/')
def landing():
    if 'userID' in session:
        return redirect(url_for('home'))
    else:
        return render_template("index.html")



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


@app.route('/login/', methods=['GET', 'POST'])
def login():     
    ## 세션 정보 있으면 home로 이동
    if 'userID' in session:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':

            id = request.form['userID']
            pw = request.form['password']

            base.db.session.query(Users).order_by(Users.user_id.desc())
            user = Users.query.filter(Users.id == id).first()
            
            header = 'login'

            ##로그인 정보 일치하는 지 확인
            ##1) 아이디 검색
            if user is None:
                current_app.logger.info('%s, / : none id' % (id))
                return render_template("/login/login.html", status=header, message='ID_NOT_FOUND')
            
            ##2) 아이디+비밀번호 검색
            if user.pw != pw :
                current_app.logger.info('%s, / : PASSWORD_NOT_FOUND ' % (id))
                return render_template("/login/login.html", status=header, message='PASSWORD_NOT_FOUND')
            
            session["userID"] = user.user_id
            current_app.logger.info("로그인 성공")
            return redirect(url_for('home'))
        
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

            test_query = base.db.session.query(Users).order_by(Users.user_id.desc())
            test_query =test_query.first()
            
            users = {}
            users['user_id'] = int(test_query.id) + 1
            users['id'] = request.form['userID']
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
    id = request.form['userID']
    
    base.db.session.query(Users).order_by(Users.user_id.desc())
    user = Users.query.filter(Users.id == id).first()
    ## 1)data(유저가 입력한 아이디) 중복인지 확인
    if user is None:
        code = "0"
    ## 2)중복이면 code = "1"
    else:
        code = "1"
    return code

#from models.user import Books 
#from schemas.user import BooksSchema

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


def getSharingUser(book_id, user):
    bookShareList = []
    userLoc = (user[0], user[1])
    sharingUser = base.db.session.query(Sharings).join(Sharings.user).filter(Sharings.book_id == book_id).all()

    for row in sharingUser:
        sharingLoc = (row.user.lat, row.user.long)
        if  haversine(userLoc, sharingLoc) <= 10 :
            sharingUser = {}
            sharingUser['nickname'] = row.user.nickname
            sharingUser['email'] = row.user.email
            sharingUser['lat']=row.user.lat
            sharingUser['long']=row.user.long
            bookShareList.append(sharingUser)

    return bookShareList

@app.route('/bookInfo/<int:id>')
def book_info(id):
    if 'userID' in session:
        header='logout'
        userID = session["userID"]
        
        # 해당 책의 ID를 이용하여 책 상세 정보를 가져온다.
        book = base.db.session.query(Books).filter(Books.book_id == id).first()
        if book:
            author = base.db.session.query(Authors).filter(Authors.author_id == book.author_id).first()
            book.authorName = author.name
            
            ## 유저가 이전에 기록한 평점이 있는지 확인
            ## 있다면 rating 지정
            
            rating = Ratings.query.filter(Ratings.user_id == userID, Ratings.book_id == id).first()
            if rating is None:
                userRating = 0
            else :
                userRating = rating.rating
            
            ## 유저 위치 정보(북 쉐어 찾을 때 지도 중심 설정)
            user = Users.query.filter(Users.user_id == userID).first()
            #print(user.lat, user.long)
            userLoc = [user.lat, user.long]
            #userLoc = ["37.553091", "126.845341"]

            ## 북 쉐어 리스트
            bookShareList = getSharingUser(id, userLoc)

            ## 리뷰 리스트
            review = base.db.session.query(Ratings).join(Ratings.user).join(Ratings.review).filter(Ratings.book_id == id).all()
            reviewList = []
            for row in review:
                review = {}
                review['nickname'] = row.user.nickname
                review['rating'] = row.rating
                review['review'] = row.review.review_TEXT
                reviewList.append(review)

            return render_template("/bookinfo/bookinfo.html", status=header, book=book, id=id, userRating=userRating, userLoc = userLoc, bookShareList=bookShareList, reviewList=reviewList)
        else:
            return render_template("/error/404.html")
    else:
        return redirect(url_for('landing'))


@app.route('/deleteRating/', methods=['POST'])
def deleteRating():
    userID = session["userID"]
    bookID = request.form['bookID']
   
    Ratings.query.filter(Ratings.user_id == userID, Ratings.book_id == bookID).delete()
    base.db.session.commit()

    print("delete : ", userID, bookID)
    
    return "Delete Rating"

@app.route('/insertRating/', methods=['POST'])
def insertRating():
    userID = session["userID"]
    bookID = request.form['bookID']
    rating = request.form['rating']

    test_query = base.db.session.query(Ratings).count()

    ratings = {}
    ratings['rating_id'] = int(test_query) + 1
    ratings['user_id'] = session["userID"]
    ratings['book_id'] = request.form['bookID']
    ratings['rating'] = request.form['rating']
    ratings = Ratings(** ratings)
    base.db.session.add(ratings)
    base.db.session.commit()

    print("insert : ", userID, bookID, rating)
    return "Insert Rating"

@app.route('/writeReview/<int:id>', methods=['POST'])
def writeReview(id):
    userID = session["userID"]
    review = request.form['reviewArea']
    test_query = base.db.session.query(Reviews).count()
    review_id = int(test_query) + 1
    
    ##rating 테이블과 연결
    rating = Ratings.query.filter(Ratings.user_id == userID, Ratings.book_id == id).first()
    rating.review_id = review_id
    base.db.session.commit()
    
    ##review table에 저장
    reviews = {}
    reviews['review_id'] = review_id
    reviews['review_TEXT'] = request.form['reviewArea']
    reviews = Reviews(** reviews)
    base.db.session.add(reviews)
    base.db.session.commit()
    
    print("review : ", id, userID, review)
    return redirect(url_for('book_info', id=id))

@app.route('/search/', methods=['GET', 'POST'])
def search():
    if 'userID' in session:
        header='logout'

        if request.method == 'GET':
            return render_template("/search/search.html", status=header, searched=False)
        
        else:
            ##검색창 입력단어
            searchWord = request.form["searchWord"]
            bookList = base.db.session.query(Books).filter(Books.title.like("%"+searchWord+"%")).all()
            #book_data = BooksSchema().dump(book_data, many=True)
            
            return render_template("/search/search.html", status=header, searched=True, bookList=bookList)


    else:
        return redirect(url_for('landing'))
    


@app.route('/share/', methods=['GET', 'POST'])
def share():
    if 'userID' in session:
        userID = session["userID"]
        header='logout'

        sharing = base.db.session.query(Sharings).join(Sharings.book).filter(Sharings.user_id == userID).all()
        bookList = []

        for row in sharing:
            book = {}
            book['book_id'] = row.book_id
            book['title'] = row.book.title
            book['image_url'] = row.book.image_url
            bookList.append(book)
        
        return render_template("/share/share.html", status=header, bookList=bookList)

    else:
        return redirect(url_for('landing'))    

@app.route('/searchShareBook/', methods=['POST'])
def searchShareBook():
    data = request.form['searchWord']

    search = base.db.session.query(Books).join(Books.author).filter(Books.title.like("%"+data+"%")).all()
    searchList = []

    for row in search:
        book = {}
        book["id"] = row.book_id
        book["title"] = row.title
        book['author'] = row.author.name
        searchList.append(book)

    return render_template("/share/tableCell.html", searchList=searchList)

@app.route('/addShareBook/<string:book_id>', methods=['GET'])
def addShareBook(book_id):
    userID = session["userID"]

    test_query = base.db.session.query(Sharings).count()
       
    ##sharings table에 저장
    sharing = {}
    sharing['share_id'] = int(test_query) + 1
    sharing['user_id'] = userID
    sharing['book_id'] = book_id
    sharing = Sharings(** sharing)

    base.db.session.add(sharing)
    base.db.session.commit()

    print("ADD : ", book_id, userID)
    return redirect(url_for('share'))  

@app.route('/deleteShareBook/<string:book_id>', methods=['GET'])
def deleteShareBook(book_id):
    userID = session["userID"]

    Sharings.query.filter(Sharings.user_id == userID, Sharings.book_id == book_id).delete()
    base.db.session.commit()

    print("DELETE : ", book_id, userID)
    return redirect(url_for('share')) 


app.debug = True
app.run('127.0.0.1', port=5500)