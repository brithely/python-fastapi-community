# python-fastapi-community

### 개발환경
python 3.9.13
mysql 8.0.28
fastapi 0.78.0

### 실행방법
    export DB_HOST=mysql
    export DB_PASSWORD=test1234
    export DB_USER=root
    export DB_DATABASE=test_db
    export DB_PORT=3306
    docker-compose up

### ERD 다이어그램
![스크린샷 2022-07-13 오후 11 11 48](https://user-images.githubusercontent.com/37111838/178754641-662f6d02-b67a-45ec-ad77-579ba95e288f.png)


### API Endpoint
- GET /api/posts
- POST /api/posts
- DELETE /api/posts/{post_id}
- PUT /api/posts/{post_id}
- GET /api/posts/{post_id}/comments
- POST /api/posts/{post_id}/comments


### API Docs
http://localhost:8000/docs
