# python-fastapi-community

### 개발환경
docker 이미지 활용
python 3.9.13
mysql 8.0.28
fastapi 0.78.0

### 실행방법
    export DB_HOST=localhost
    export DB_PASSWORD=test1234
    export DB_USER=root
    export DB_DATABASE=test_db
    export DB_PORT=3306
    docker-compose up


### API Endpoint
GET /api/posts
POST /api/posts
DELETE /api/posts/{post_id}
PUT /api/posts/{post_id}

GET /api/posts/{post_id}/comments
POST /api/posts/{post_id}/comments


