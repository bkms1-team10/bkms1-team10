from flask import session, render_template ,request , redirect , url_for , current_app
from server import app ,db
from models.user import Users
from schemas.user import UsersSchema


@app.route('/login', methods=['GET', 'POST'])
def login():     
    ## 세션 정보 있으면 home로 이동


    if request.method == 'POST':
        data = request.form

        id = data['id']
        pw = data['pw']
        db.session.query(Users).order_by(Users.id.desc())
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


    data = request.form

    test_query = db.session.query(Users).order_by(Users.id.desc())
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
    db.session.add(user)
    db.session.commit()


    return 'true'


@app.route('/idCheck/', methods=['POST'])
def idCheck():
    data = request.form['userID']
    code = "0"
    ## 1)data(유저가 입력한 아이디) 중복인지 확인
    ## 2)중복이면 code = "1"
    return code