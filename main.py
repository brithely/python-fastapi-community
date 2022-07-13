from fastapi import FastAPI

from app.community.endpoints import api

description = """
커뮤니티 앱 서버

테이블 설명

## Author
게시글 및 댓글 작성 시 Author 테이블에 입력 (존재하는 경우에는 기존 id 사용)

## Keyword
게시글 및 댓글 작성 시 알람을 보낼 키워드

## AuthorKeyword
해당 키워드로 알람 설정이 되어있는 작성자 테이블
키워드 더미데이터 test0 ~ test9 까지 존재
알림 발송 시 print 메세지 출력

## Post
게시글은 목록, 작성, 삭제, 수정이 가능합니다.

수정 및 삭제 시에는 게시글의 패스워드가 일치하여만 수정 및 삭제 가능합니다.

## Comment
댓글은 목록, 작성이 가능합니다.

댓글의 구조는 depth 형태로 나타내며 depth 1이 최상단의 댓글입니다.

ex)
댓글 (depth 1)\n
댓글의 대댓글 (depth 2)\n
댓글의 대댓글의 대댓글 (depth 3)\n
댓글의 대댓글의 대댓글의 대댓글 (depth 4)\n
댓글2\n
"""

app = FastAPI(title="CommunityApp", description=description)

app.include_router(api.router, prefix="/api")
