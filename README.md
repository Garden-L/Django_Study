# Django_Study

## 파일구조
* ProjectName/
    * conf/
        * \_\_init\_\_.py
        * settings.py
        * urls.py
        * wsgi.py
    * app1
        * \_\_init\_\_.py
        * settings.py
        * urls.py
        * wsgi.py
    * app2
    * manage.py
    * sqlite3

### 예시
```code
$ django-admin startproject conf . //현재 디렉토리에 프로젝트 생성, 기본세팅은 conf 디렉토리에서 수행
```

* DatabaseSchool/
    * conf/
        * \_\_init\_\_.py 
        * asgi.py
        * settings.py
        * urls.py #url 연결파일
        * wsgi.py
    * manage.py

<br></br>

## Templates
```python
BASE_DIR = Path(__file__).resolve().parent.parent  #프로젝트 파일의 절대값 c:\...\DatabaseSchool

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # 템플릿 엔진 설정 : Django는 기본적으로 Jinja2 지원
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # 템플릿을 담을 경로 설정, 여러 경로 등록 시 리스트 순서대로 템플릿을 탐색
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
## App
Django에서는 각 등록된 앱에 대한 다양한 명령어 (makemigrations, migrate 등) 실행 하려면 conf/setting.py 파일 INSTALLED_APPS에 설치한 앱의 'app이름'Config 클래스를 등록하여야 한다.

```python
$ django-admin startapp account #account 앱을 생성

#setting.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig', #AccountConfig 클래스 등록, AccountConfig클래스 내부에 name 멤버변수 값이 설정됨
]
```


## URL
### url경로
사용자가 locallhost:8000/account 요청
conf/url.py 파일에서 account경로 확인, 특정앱으로 이동시키려면 include(app이름)
```python
from django.urls import path, include

extra_urlpatterns =[
    path('file/', views.path)
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')) #account/urls.py 파일로 이동
    path('extra/, include(extra_urlpatterns)) #리스트 변수가능
    path('list/, include([path('page1', views.page1) , path('page2', views.page2)]) #리스트 값 자체로 넣는 것 또한 가능
]
```


## Views

### Views 가이드라인
* 뷰 코드의 양은 적으면 적을수록 좋다.
* 뷰 안에서 같은 코드의 반복적 사용을 지양하자
* 뷰는 프레젠테이션 로직에서 관리, 비즈니스 로직은 모델에서 처리, 특별한 경우 폼에서 처리
* 뷰는 간단 명료해야한다.
* 403, 404,500 에러 핸들링에는 CBV를 이용하지 않는다. FBV로 처리하자
* 믹스인(Mixin)은 간단 명료해야 한다.


뷰의 구현 방식은 CBV(Class Based View)와 FBV(Function Based View)로 나뉜다.

### FBV
```python
#urls.py
urlpatterns = [
    path('', views.index, name='index'),
]
```
```python
# views.py
def index(request):
    if request.method == 'POST':         
        # POST 요청일경우 
    else:         
        # POST 요청이 아닐 경우
```
* 장점
  * 간단하고 가독성이 좋다
  * 데코레이터 사용이 명료하다
* 단점
  * 중복되는 코드가 생길 가능성이 매우 높다. 
  * 코드의 재사용이 어렵다.

## Models
```python
# user 데이터베이스 모델 생성과정

class User(models.Model): #모델생성시 복수형태로 쓰지 않음
   name = models.CharField(max_length) #최대 Max_legnth까지 문자 저장가능 -> TextInput 폼 
        = models.TextField() # Django docs에서도 방대한 text는 textfield 이용하길 권장
   
   class Meta:
      db_table = "user" #이 설정을 안하면 table 이름이 ("app이름"_객체명)형태로 저장된다
      ordering = ['name'] # 검색된 객체는 name순으로 오름차순으로 정렬된다 (내림차순은 "-name")
      
      
$ python manage.py makemigrations #마이그레이션 생성- 단순히 기록용으로 생성 0001_~.py 
$ python manage.py migrate #자동으로 마지막으로 생성된 마이그레이션을 데이터베이스에 등록한다. 실제 
```
### migrations 초기화
데이터베이스를 초기화 시키고 싶으면 전체 앱의 migrations 폴더에서 \_\_init\_\_.py를 제외한 생성한 기록과 sqlite3를 사용하는 경우 db.sqlite3까지 모두 삭제한다.

* 장고는 모델생성시 자동으로 id 값을 부여한다. tuple을 추가할 때마다 자동생성

### options
#### choices
```python
#사용자가 선택하도록 models을 만들 때 choices로 제한 할 수 있음
RES=( (1, '학생'), (2, '교수') )
respon = models.CharField(max_lenght=2, choices=RES) 
```

#### unique
똑같은 값이 들어가지 않도록 unique 제약조건을 설정
```python
email = models.CharField(max_length=50, unique=True)
```
#### unique
필드를 primary key로 설정. primary key로 설정 시 장고에서 자동 생성해주는 id필드가 생성되지 않음
```python
jumin = models.IntegerField(primary_key=True) 

#장고가 자동으로 등록해주는 id 값 필드 
id = models.AutoFeild(primary_key=True) #자동증가 필드, 값을 추가 할 때마다 1씩 자동 증가
```

## ORM(Object-Relation Mapping)
객체(Object)와 관계형 데이터베이스(Relation)를 연결(Mapping)해주는 것을 의미한다.
테이블과 객체를 연결- Student라는 이름을 가진 테이블은 Student 객체로 연결(Mapping), 장고에서 정확한 테이블 이름은 
'app명_table명'이다. 

### 데이터 조회(READ) \[장고 docs: Field lookups\]
#### -table.objects.all() == SQL : SELECT * FROM table;
return 값: <QuerySet [\<table objects\>, \<table objects\> ... \<table objects\>]>' </br> 전체 tuple을 리스트형태로 반환
```python 
query_set = Table.objects.all() 
for obj in query_set: #리스트 형태이기 때문에 반복문 사용가능
  print(obj) #<table objects (pk)>
```
#### - table.objects.filter(*args, **kwargs) == SELECT * FROM table where (조건);
예시 : table.object.filter(id=10, grade=100) == SELECT * FROM table where id=10 and grade=100;
<br></br>
#### - table.objects.exclude(*args, **kwargs) == SELECT * FROM table where not (조건);
예시 : table.object.exclude(id=10, grade=100) == SELECT * FROM table where not(id=10 and grade=100);
<br></br>
#### - table.objects.get(*args, **kwargs) == SELECT * FROM table where not (조건);
예시 : table.object.get(id=10, grade=100) == SELECT * FROM table where not(id=10 and grade=100);

## CBV
### TemplateResponseMixin 클래스
사용자 응답 관련 클래스 
```python
#멤버변수
   template_name  #render할 template 위치
   template_engin #render할때 사용할 engin
   content_type   #context할 것
```
# 로그인 구현 (AbstractBaseUser 상속)
AbstractBaseUser를 상속하는 경우 Django의 인증 시스템은 사용하면서도 개발자가 직접 원하는 로그인 방식을 지정할 수 있다.

## AbstractBaseUser
AbstractBaseUser는 기본적으로 id, password, last_login 속성을 추가한다. 이때 id는 사용자가 직접 설정한 로그인할 때 쓰는 id가 아니라 장고에서 기본적으로 추가해주는 id이다. primary_key속성을 지정해주면 id속성을 만들지 않는다.

### User 데이터베이스 구현예제
```python 

class User(AbstractBaseUser):
    RESP=(
        ('student', '학생'),
        ('prof', '교수'),
    )
    
    incomingid = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    resp = models.CharField(max_length=20, choices=RESP)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'incomingid'
    EMAIl_FIELD = 'email'
    REQUIRED_FIELDS =['name', 'email']
    object = UserModel()
    
    class Meta:
        db_table = "user"
        
    def __str__(self):
        return self.name

    def has_perm(self, a):
        return True
    
    def has_module_perms(self, app_label):
        return True

```
### USERNAME_FIELD 
고유 식별자로 사용되는 자용자 모델의 필드 이름을 설명하는 문자열 사용자가 직접 백엔드를 다루지 않는 이상 unique한 값이여야 한다
```python
 incomingid = models.CharField(max_length=10, unique=True)
```
AbstractBaseUser의 get_username 함수로 속성값 가져온다.

#### USERNAME_FEILD가 unique하지 않을 시

```code
$ python manage.py createsuperuser  #슈퍼유저생성

#에러 출력
   account.User: (auth.E003) 'User.name' must be unique because it is named as the 'USERNAME_FIELD'.
```

### EMAIL_FILED
이메일 필드가 있을 시 설정한다. 
AbstractBaseUser의 get_email_field_name 함수로 속성값을 가져온다.

```python
#Django AbstractBaseUser클래스 
#위치 : from django.contrib.auth.models import AbstractBaseUser

class AbstractBaseUser(models.Model):
    password = models.CharField(_("password"), max_length=128)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    
...(생략)
```

### REQUIRED_FIELDS
유저생성시 꼭 입력 받아야하는 속성 값을 설정한다. USERNAME_FIELD와 password는 자동 추가 되므로 생략해야한다. 넣으면 오히려 문제가된다.

### objects
BaseUserManager 상속을 무조건 구현해야하며, User클래스에 설정해야한다.

### admin과 연동
직접 작성한 User모델을 admin에서 사용하고 싶으면 필수 등록 항목이있다

#### is_staff 
#### is_active
#### has_perm(perm, obj=None):
#### has_module_perms(app_label):
#### has_perm과 has_module_perms 는 PermissionMixed를 상속받으면 여기에 구현하는 것이 맞음

### BaseUserManager
AbstractBaseUser를 상속받은 경우 BaseUserManager 또한 구현해야 한다.
구현 필드가 장고의 디폴트 User와 다를경우
create_user
create_superuser 함수를 추가해야한다. 장고에서 유저를 생성할때 이 함수를 호출하는 듯
AbstractBaseUser를 상속받은 클래스에 objects = BaseUserManager상속클래스() 설정을 해야한다.
### 구현










# python
## dic
key와 value의 조합으로 된 자료구조

D = {"name":"LJW", }

### get(key)
```python
print(D.get("name")) 
#출력
"LJW"
```

#Pandas

## 비교

### DataFrame.compare(other, align_axis=1, keep_shape=False, keep_equal=False)
데이터 프레임과 비교. 단, 데이터 프레임의 행과 열의 수가 같아야 비교가 됨(ValueError)

```python
#예제 데이터
df = pd.DataFrame(
    {
        "col1": ["a", "a", "b", "b", "a"],
        "col2": [1.0, 2.0, 3.0, np.nan, 5.0],
        "col3": [1.0, 2.0, 3.0, 4.0, 5.0]
    },
    columns=["col1", "col2", "col3"],
)

#출력
col1	col2	col3
0	a	1.0	1.0
1	a	2.0	2.0
2	b	3.0	3.0
3	b	NaN	4.0
4	a	5.0	5.0

df2 = df.copy()
df2.loc[0, 'col1'] = 'c'
df2.loc[2, 'col3'] = 4.0

#출력
	col1	col2	col3
0	c	1.0	1.0
1	a	2.0	2.0
2	b	3.0	4.0
3	b	NaN	4.0
4	a	5.0	5.0
```

#### other : DataFrame
#### align_axis : 0 == "index", 1=="columns", 기준점을 행값으로 할지 열값으로 할지 결정, default="columns"
#### keep_shape : 테이블의 모양을 비교전과 유지할건지,
#### keep_equal : 기본적으로 틀린값만 반환하고 맞는 값은 NaN 반환, True로 설정시 맞는 값도 반환


```python
#columns 기준
df.compare(df2, align_axis = 1, keep_shape = False, keep_equal=False) 

#출력
  col1      	col3
  self	other	self	other
0	a	   c	   NaN	NaN
2	NaN	NaN	3.0	4.0
```


