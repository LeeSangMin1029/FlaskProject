# FlaskProject
**플라스크 웹 개발**은 외국 도서를 번역한 책이다. 아마 인터넷에서 글을 올리다가 이렇게 책으로 출간한 것 같다. 

오탈자 나와있는 곳:[flasky](https://www.flaskbook.com/)

git주소:[git](https://github.com/miguelgrinberg/flasky)

blog주소:[blog](https://blog.miguelgrinberg.com/)

원래 README에는 버그, 사용법, 배포자 등을 작성하지만 아직 그 단계는 아니니 공부한 것을 작성하자.
참고로 clone해서 애플리케이션을 실행시키려면 python을 실행시킬 수 있는 환경에서 python run.py로 실행하면 된다.
## 18/11/19
requirements.txt 파일은 주기적으로 업데이트 필요, database(SQLAlchemy)와 test(unittest)할 파일 추가함. 만약 온라인 상에서 파일을 변경하였다면 pull 명령어를 사용하여 충돌을 피해야 함
이거는 내가 전에 sqlalchemy를 처음 사용하면서 경험했던 pylint와 관련된 issue : [issue related to pylint](https://github.com/Microsoft/vscode-python/issues/292)
## 18/11/20
generate_password_hash(password, options..)는 사용자로부터 입력받은 password를 데이터베이스에 저장할 수 있는 문자열인 password_hash를 리턴하는 함수이다.

check_password_hash(hash, password)는 위 함수에서 hash된 password를 사용자가 입력한 password와 비교해서 맞으면 True 틀리면 False를 리턴한다.

책에서 로그인 폼을 추가하는 부분을 공부하던 도중 오류가 나서 애를 먹었다. 
예를 들면 
> {% if current_user.is_authenticated %} <- 이게 맞는 문법인데 
> {% if current_user.is_authenticated() %} 이런식으로 혼란을 준다거나...

정작 git checkout 8c를 입력해서 해당 부분을 검토하면 괄호가 사라져있고... 내용을 잘 진행하다가 이런 사소한 문제 때문에 힘들다. 
requirements.txt는 일단 계속 업데이트를 하고 있는데, 이 파일이 필요한 이유는 다른 사람들과 내가 협업을 할 때 내 앱(그러니까 프로젝트)이 어떤 라이브러리 버젼을 사용하는지 적어놓지 않으면 혼란이 오기 때문인것 같다.

## 18/11/22
새로운 사용자를 등록하는 폼을 추가했다. 상속받는 클래스를 왜 FlaskForm으로 정했냐면, 앱을 실행을 시켰는데 계속 에러? 가 발생했다. stackoverflow에서 오류를 찾아보니 Form은 old version 이라서 FlaskForm을 더 권장한다고 해서 바꿨더니 사라졌다. 내가 찾아서 오류를 고쳤던 글과는 다르지만 비슷한 링크라도 달아둬야겠다. 링크[Form_관련_stackoverflow](https://stackoverflow.com/questions/22873794/attributeerror-editform-object-has-no-attribute-validate-on-submit/22873885#22873885)
코드는 아래와 같다.
```python
class RegistrationForm(FlaskForm):
    email=StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username=StringField('Username', validators=[Required(), Length(1, 64), 
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, '
        'numbers, dots or underscores')])
    password=PasswordField('Password',validators=[Required(),
        EqualTo('password2', message='Passwords must match.')])
    password2=PasswordField('Confirm password', validators=[Required()])
    submit=SubmitField('Register')
```
username의 validators중에 Regexp를 보면 문자, 숫자, 밑줄, 점으로만 구성되어 있는지를 확인하는 것이고, 옆에 두개의 인수 **0**과 문자열**Usernames must have only letters, numbers, dots or underscores** 는 각각 정규식 플래그와 email의 정해진 입력양식을 벗어날 경우 보여주는 에러 메시지이다.
password는 EqualTo만 보면 된다. EqualTo는 사용자가 입력한 첫 번째 필드인 password를 기준으로 password2 필드와 비교해서 두 password가 다르면 **Passwords must match.** 라는 메시지를 보여준다. 또 코드를 보자. 위와 이어지는 코드이다.

```python
def validate_email(self, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')
    
def vaildate_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username already in use.')
```
위 두 개의 함수는 사용자가 입력한 email과 username이 있는지 확인하는 custom validator라고 한다. validate_필드이름 이런식으로 정의를 하게 되면 validator를 정의하도록 추가적으로 호출된다고 한다. raise는 강제로 예외를 발생시키는 파이썬 예외 관련된 문법이다.
이 Form은 /templates/auth/register.html에서 wtf.quick_form()으로 렌더링을 해야한다.
아래는 사용자를 추가하는 view 함수이다. 
```python
@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,
                username=form.username.data,
                password=form.password.data)
        db.session.add(user)
        flash('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
```
사용자가 계정을 추가하는 버튼 'Register'버튼을 누르면 자동으로 데이터베이스에 사용자의 정보가 저장이 된다.

## 18/11/25
영어 공부도 하고, 플라스크 책말고 다른 파이썬 책을 읽다보니 시간이 벌써 3일이 지나버렸다.
공부한 내용은 별로 안되지만 일단 정리해봤다. 보통 계정이 필요한 웹사이트에서는 처음에 가입을 할 때 이메일, 아이디, 비밀번호를 쳐서 계정을 생성한다. 이 때 가입을 하면 웹사이트 상단, 하단 등 아니면 새로 페이지를 생성해서 사용자에게 무슨 인증을 받으라고 한다. 그전까지는 일부 콘텐츠를 이용하지 못한다거나 그러한 제약 부분이 존재한다는 것? 내가 생각하기에는 이 인증부분이 내가 지금 배우고 있는 것과 똑같은 부분이지 않을까 생각한다. 책에서도 이해가 되지는 않지만 얼추 비슷한 내용이 있다.
> 애플리케이션에서는 이메일 주소를 검증하기 위해 사용자가 가입 즉시 확인 이메일을 사용자에게 전송한다. 새로운 계정은 처음에는 사용자에게 전송한 이메일이 확인될 때까지 미확인 상태로 유지한다. 계정 확인은 확인 토큰을 포함하고 있는 특정 URL 링크를 클릭하도록 하는 과정을 포함한다.

http://www.example.com/auth/confirm/<id> 이런식으로 계정확인을 할 경우 문제점이 있다. 보안상으로도 안전하지 못하고 사용자가 계정을 확인하는 링크를 알고있다면 사용자 id에 임의의 숫자를 입력해서 아무렇게나 계정을 확인할 수 있게 된다. 어떻게 해결하냐면 사용자 id를 포함하는 보안 토큰으로 대체하는데 이때 **itsdangerous** 패키지를 사용하면 된다고 한다.

```python
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import curren_app
from flask_login import UserMixin
from . import db
#...

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    confirmed=db.Column(db.Boolean, default=False)
    #...

    def generate_confirmation_token(self, expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})
    
    def confirm(self, token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True
```

**TimedJSONWebSignatureSerializer**는 이름이 너무 길어서 **Serializer**로 수정한다. **Serializer**클래스는 시간 만료 정보를 사용하여 JWS를 생성한다. 이 클래스의 생성자는 인수로 위와 같이 키(SECRET_KEY), 만료시간(expiration) 이렇게 넣어줄 수 있다. SECRET_KEY는 config.py에 정의되어 있는 사용자 정의 키다. expiration은 초 단위로 토큰의 만료시간을 정해주는 인수다. generate_confirmation_token() 메소드는 한 시간의 기본 검증 시간을 갖고 토큰을 생성한다. (한 시간이 지난 토큰을 가지고 계정확인을 한다면 아마 오류가 나겠지?)
dumps() 메소드는 인수로 주어진 데이터를 위한 signature password(임의적으로 바꿀 수 없는 암호)를 생성하고 **\'confirm':self.id**해당 데이터를 토큰 문자열로서 signature를 직렬화한다. (무슨 소린지 모르겠지만 하다보면 알게되겠지...)

토큰을 디코딩하려면 **Serializer**가 제공하는 loads() 메소드를 이용하면 된다. loads() 메소드를 이용해서 정의한 함수가 confirm() 메소드이다. 해당 메소드는 토큰을 검증하고 맞으면 True값을 반환하는 기능을 가지고 있다.
만약 예를 들어 어떤 유저의 토큰을 추출하려면 다음과 같이 하면 된다. 해당 명령은 python shell에서 실행했다.() 주의할 점은 loads() 메소드는 올바르지 않은 토큰이 주어지거나 만료된 토큰이 주어진다면 예외가 발생하니 위와 같이 예외처리를 잘 해두면 예상치 못했던 에러를 방지 할 수 있다.

```python
User.query.filter_by().first()
lsm=User.query.filter_by().first()
token=lsm.generate_confirmation_token()
token
# 이와 같이 토큰이 성공적으로 추출된다. 길어서 생략
b'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU0MzE0NTM5MywiZXhwIjoxNTQzMTQ4OTkzfQ.eyJjb25maXJtIjoxfQ.......'
# 해당 토큰이 맞는지 확인하려면 위에 정의해놓은 메소드를 사용하면 된다.
lsm.confirm(token)
True
```
## 18/11/26
이것저것 했다. 계정확인을 하는 이메일이 오지가 않아서 하루종일 헤매다가 해결완료했다.

## 18/11/28
좀 늦은 시간에 공부를 시작해서 간단하게 패스워드 업데이트(변경)하는 부분만 완료했다. 내가 코드를 먼저 작성하고 애플리케이션을 실행해봤더니 에러가 발생했다. 고민을 하다가 checkout해서 코드를 보니 내 코드와 다른 부분이 있었다. 나는 form 부분에서 password, submit field만 필요할 줄 알았는데 더 많이 필요로 했다. 앞으로 이런 부분을 틀리지 않도록 숙지 해야겠다. 아마 이 password 변경하는 코드는 나중에 좀 더 진도를 나가면 쓸데가 있을것 같다.
