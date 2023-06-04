from flask import session, render_template ,request , redirect , url_for
from server import app ,db
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

    if 'userID'not in session:
        return redirect(url_for('landing'))
    
    else:

        book_data = db.session.query(Books).filter(Books.book_id == id).first()
        return render_template("/bookinfo/bookinfo.html", book = book_data)
    