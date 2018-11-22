# FlaskProject
## 참고하는 책
**플라스크 웹 개발**이라는 외국 도서를 번역한 책이다. 아마 인터넷에서 글을 올리다가 이렇게 책으로 출간한 것 같다. git과 blog를 참고하면 좋다.
[git](https://github.com/miguelgrinberg/flasky)
[blog](https://blog.miguelgrinberg.com/)
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