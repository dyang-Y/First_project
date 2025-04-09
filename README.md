# Django CRUD 게시판

간단한 Django 기반 CRUD(Create, Read, Update, Delete) 게시판 웹 애플리케이션입니다.

## 기능

- 게시글 목록 보기
- 게시글 상세 보기
- 게시글 작성
- 게시글 수정
- 게시글 삭제

## 기술 스택

- Python 3.9+
- Django 4.2
- Bootstrap 5
- SQLite (개발)

## 설치 및 실행 방법

1. 저장소 클론
```
git clone https://github.com/dyang-Y/First_project.git
cd First_project
```

2. 의존성 설치
```
pip install django
```

3. 데이터베이스 마이그레이션
```
python manage.py migrate
```

4. 개발 서버 실행
```
python manage.py runserver
```

5. 웹 브라우저에서 `http://127.0.0.1:8000` 접속

## 관리자 계정 생성

```
python manage.py createsuperuser
```

관리자 페이지는 `http://127.0.0.1:8000/admin/`에서 접근 가능합니다. 