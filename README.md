# FlaskProject
## 18/11/19
requirements.txt 파일은 주기적으로 업데이트 필요, database(SQLAlchemy)와 test(unittest)할 파일 추가함. 만약 온라인 상에서 파일을 변경하였다면 pull 명령어를 사용하여 충돌을 피해야 함
이거는 내가 전에 sqlalchemy를 처음 사용하면서 경험했던 pylint와 관련된 issue : [issue related to pylint](https://github.com/Microsoft/vscode-python/issues/292)
#### 자제 해야하는 command
git reset --hard 돌아갈 commit 번호
## 18/11/20
generate_password_hash(password, options..)는 사용자로부터 입력받은 password를 데이터베이스에 저장할 수 있는 문자열인 password_hash를 리턴하는 함수이다.
check_password_hash(hash, password)는 위 함수에서 hash된 password를 사용자가 입력한 password와 비교해서 맞으면 True 틀리면 False를 리턴한다.
책에서 로그인 폼을 추가하는 부분을 공부하던 도중 오류가 나서 애를 먹었다. 
예를 들면 
> {% if current_user.is_authenticated %} <- 이게 맞는 문법인데 
> {% if current_user.is_authenticated() %} 이런식으로 혼란을 준다거나...
정작 git checkout 버전넘버(8c)를 입력해서 해당 부분을 검토하면 괄호가 사라져있고... 내용을 잘 진행하다가 이런 사소한 문제 때문에 힘들다. 
requirements.txt는 일단 계속 업데이트를 하고 있는데, 이 파일이 필요한 이유는 다른 사람들과 내가 협업을 할 때 내 앱(그러니까 프로젝트)이 어떤 라이브러리 버젼을 사용하는지 적어놓지 않으면 혼란이 오기 때문인것 같다.
