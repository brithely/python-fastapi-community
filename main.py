from fastapi import FastAPI

from app.community.endpoints import api

description = """
커뮤니티 앱 서버

## Author
게시글 작성 시 

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
