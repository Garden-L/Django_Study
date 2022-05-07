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

## 로그인 구현 (User 상속 받지 않고 구현)
```code
$ django-admin startapp account //계정 관리 app 생성, 

DatabaseSchool/
    conf/
    account/
        migrations/ #데이터베이스의 관한 기록관리- DB만 전용으로하는 github 기능
            __init__.py
        __init__.py 
        admin.py
        apps.py
        models.py #테이블 생성 등 데이터베이스 관한 처리
        tests.py
        views.py #파싱에관한것
        urls.py #사용자가 직접생성, 계정에 관한 모든 url 연결은 conf에서 account로 넘기게 함
    manage.py
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
