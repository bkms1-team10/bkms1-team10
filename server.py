from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from app.module.data import Book, User
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/index/')
def landing():
    if 'userID' in session:
        return redirect(url_for('home'))
    else:
        return render_template("index.html")

@app.route('/login/', methods=['GET', 'POST'])
def login():     
    ## 세션 정보 있으면 home로 이동
    if 'userID' in session:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
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
            session['userID'] = request.form['userID']
            return redirect(url_for('home'))
        else:
            header='login'
            return render_template("/login/login.html", status=header)

@app.route('/idCheck/', methods=['POST'])
def idCheck():
    data = request.form['userID']
    code = "0"
    ## 1)data(유저가 입력한 아이디) 중복인지 확인
    ## 2)중복이면 code = "1"
    return code

@app.route('/logout/')
def logout():
    session.pop('userID', None)
    return redirect(url_for('landing'))

@app.route('/join/')
def join():
    if 'userID' in session:
        return redirect(url_for('home'))
    else:
        header='login'
        return render_template("/login/join.html", status=header)    

@app.route('/')
def home():
    if 'userID' in session:
        header='logout'

        ##데이터 받아오기 예시
        ##책 리스트
        seriesList = {}

        title1 = "평균 별점이 높은 책"
        seriesList[title1] = []

        book1 = Book()
        book1.book_id = "001"
        book1.title="해리포터와 마법사의 돌"
        book1.average_rating="3.5"
        seriesList[title1].append(book1)

        book2 = Book()
        book2.book_id = "002"
        book2.title="해리포터와 비밀의 방"
        book2.average_rating="4.5"
        seriesList[title1].append(book2)

        book3 = Book()
        book3.book_id = "003"
        book3.title="해리포터와 아즈카반의 죄수"
        book3.average_rating="4.0"
        seriesList[title1].append(book3)

        book4 = Book()
        book4.book_id = "004"
        book4.title="해리포터와 불의 잔"
        book4.average_rating="5.0"
        seriesList[title1].append(book4)

        title2 = "취미"
        seriesList[title2] = []

        book5 = Book()
        book5.book_id = "001"
        book5.title="해리포터와 마법사의 돌"
        book5.average_rating="3.5"
        seriesList[title2].append(book5)

        book6 = Book()
        book6.book_id = "002"
        book6.title="해리포터와 비밀의 방"
        book6.average_rating="4.5"
        seriesList[title2].append(book6)

        book7= Book()
        book7.book_id = "003"
        book7.title="해리포터와 아즈카반의 죄수"
        book7.average_rating="4.0"
        seriesList[title2].append(book7)

        book8 = Book()
        book8.book_id = "004"
        book8.title="해리포터와 불의 잔"
        book8.average_rating="5.0"
        seriesList[title2].append(book8)

        return render_template("/home/home.html", status=header, seriesList=seriesList)
    else:
        return redirect(url_for('landing'))


@app.route('/search/', methods=['GET', 'POST'])
def search():
    if 'userID' in session:
        header='logout'

        if request.method == 'GET' :
            return render_template("/search/search.html", status=header, searched=False)

        elif request.method == 'POST':
            ##검색창 입력단어
            searchWord = request.form["searchWord"]

            ##데이터 불러오기 예시
            bookList = []
            book1 = Book()
            book1.book_id = "001"
            book1.title="해리포터와 마법사의 돌"
            book1.average_rating="3.5"
            bookList.append(book1)

            book2 = Book()
            book2.book_id = "002"
            book2.title="해리포터와 비밀의 방"
            book2.average_rating="4.5"
            bookList.append(book2)

            book3 = Book()
            book3.book_id = "003"
            book3.title="해리포터와 아즈카반의 죄수"
            book3.average_rating="4.0"
            bookList.append(book3)

            book4 = Book()
            book4.book_id = "004"
            book4.title="해리포터와 불의 잔"
            book4.average_rating="5.0"
            bookList.append(book4)
            return render_template("/search/search.html", status=header, searched=True, bookList=bookList)
    else:
        return redirect(url_for('landing'))
    
@app.route('/bookInfo/')
def bookInfo():
    if 'userID' in session:
        header='logout'
        
        ## 데이터 받아오기 예시 
        ## 도서 상세정보
        book = Book()
        book.book_id = "001"
        book.title="해리포터와 비밀의 방"
        book.author="J.K. 롤링"
        book.description="대충 해리포터 줄거리임~~"
        book.average_rating="7"

        ## 북 쉐어 리스트
        bookShareList = []
        user1 = User()
        user1.nickname = "닉네임1"
        user1.email = "aaa@bbb.ccc"
        user1.lat="37.5537"
        user1.long="126.840"
        bookShareList.append(user1)

        user2 = User()
        user2.nickname = "닉네임2"
        user2.email = "ddd@eee.ffff"
        user2.lat="37.5535"
        user2.long="126.842"
        bookShareList.append(user2)
        
        return render_template("/bookInfo/bookInfo.html", status=header, book=book, bookShareList=bookShareList)
    else:
        return redirect(url_for('landing'))
    

@app.route('/share/', methods=['GET', 'POST'])
def share():
    if 'userID' in session:
        header='logout'

        ##데이터 불러오기 예시
        bookList = []
        book1 = Book()
        book1.book_id = "001"
        book1.title="해리포터와 마법사의 돌"
        bookList.append(book1)

        book2 = Book()
        book2.book_id = "002"
        book2.title="해리포터와 비밀의 방"
        bookList.append(book2)

        book3 = Book()
        book3.book_id = "003"
        book3.title="해리포터와 아즈카반의 죄수"
        bookList.append(book3)

        book4 = Book()
        book4.book_id = "004"
        book4.title="해리포터와 불의 잔"
        bookList.append(book4)
        
        return render_template("/share/share.html", status=header, bookList=bookList)

    else:
        return redirect(url_for('landing'))    

@app.route('/searchShareBook/', methods=['POST'])
def searchShareBook():
    data = request.form['searchWord']

    ##데이터 불러오기 예시
    searchList = []
    book1 = {}
    book1["id"] = "001"
    book1["title"]="해리포터와 마법사의 돌"
    book1["author"]="J.K 롤링"
    searchList.append(book1)

    book2 = {}
    book2["book_id"] = "002"
    book2["title"]="해리포터와 비밀의 방"
    book2["author"]="J.K 롤링"
    searchList.append(book2)

    book3 = {}
    book3["book_id"] = "003"
    book3["title"]="해리포터와 아즈카반의 죄수"
    book3["author"]="J.K 롤링"
    searchList.append(book3)

    book4 = {}
    book4["book_id"] = "004"
    book4["title"]="해리포터와 불의 잔"
    book4["author"]="J.K 롤링"
    searchList.append(book4)    

    return render_template("/share/tableCell.html", searchList=searchList)

@app.route('/addShareBook/<string:book_id>', methods=['GET'])
def addShareBook(book_id):
    print(book_id);
    return redirect(url_for('share'))  


@app.route('/map/')
def map():
    return render_template("/bookInfo/map.html")

app.run(debug=True)