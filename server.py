from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

@app.route('/index/')
def landing():
    ## 세션 정보 있으면 home로 이동, 없으면 landing page 출력
    return render_template("index.html")

@app.route('/login/')
def login():
    ## 세션 정보 있으면 home로 이동
    ##status로 세션 존재여부 넘기기
    header='login'
    return render_template("/login/login.html", status=header)

@app.route('/logout/')
def logout():
    print('로그아웃 되었습니다.')
    return redirect(url_for('landing'))

@app.route('/join/')
def join():
    ## 세션 정보 있으면 home로 이동
    header='logout'
    return render_template("/login/join.html", status=header)

@app.route('/')
def home():
    ## 세션 정보 없으면 landing page 출력
    ##status로 세션 존재여부 넘기기
    header='logout'
    return render_template("/home/home.html", status=header)


@app.route('/search/')
def search():
    ## 세션 정보 없으면 landing page 출력
    ##status로 세션 존재여부 넘기기
    header='logout'
    return render_template("/search/search.html", status=header)

@app.route('/share/')
def share():
    ## 세션 정보 없으면 landing page 출력
    ##status로 세션 존재여부 넘기기
    header='logout'
    return render_template("/share/share.html", status=header)

app.run(debug=True)