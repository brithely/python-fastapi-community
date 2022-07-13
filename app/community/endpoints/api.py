from email.policy import HTTP
from typing import Union

from app.community.adapters import repository
from app.community.database import get_session
from app.community.domain import exception, model
from app.community.service_layer import services
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/posts",
    status_code=200,
    response_model=list[model.ListPost],
    description="""
- 게시물 리스트\n
- 순서는 게시글의 id 순\n
- 페이지의 크기는 최대 100까지 가능
- 검색은 q 쿼리스트링을 사용하며, 게시글의 title 또는 작성자에 해당 문자를 포함하면 검색 됨
""",
)
async def list_post(
    page: int = 1,
    page_limit: int = 10,
    q: Union[str, None] = None,
    session: Session = Depends(get_session),
):
    try:
        repo = repository.PostRepository(session)
        service = services.PostService(repo=repo)
        posts = service.get_list(q=q, page=page, page_limit=page_limit)
    except (exception.InvalidPage, exception.InvalidPageLimit):
        raise HTTPException(status_code=400, detail="잘못된 페이지 입니다.")
    return posts


@router.post(
    "/posts",
    status_code=201,
    response_model=model.ListPost,
    description="""
- 게시물 작성\n
- 패스워드는 평문으로 받아서 sha256으로 저장하도록 설정\n
- 작성자의 경우 별도의 테이블로 저장 관리 노출은 author 문자열로 노출
""",
)
async def create_post(post: model.CreatePost, session: Session = Depends(get_session)):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    try:
        post = service.add(post)
    except Exception:
        raise HTTPException(status_code=400, detail="잘못된 요청입니다.")
    else:
        text = " ".join([post.title, post.text])
        alarm_repo = repository.AlarmRepository(session)
        alram_service = services.AlarmService(alarm_repo, text)
        alram_service.send()
        return post


@router.put(
    "/posts/{post_id}",
    status_code=201,
    response_model=model.ListPost,
    description="""
- 게시물 수정\n
- 게시글 제목과 내용 수정 가능
- 패스워드는 평문으로 받아서 sha256으로 변환 후 기존 패스워드 일치하는지 여부 판단\n
- 패스워드가 일치하지 않는 경우 에러 발생
""",
)
def update_post(
    post: model.UpdatePost, post_id: int, session: Session = Depends(get_session)
):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    try:
        post = service.update(post_id, post)
    except exception.NotExistPost:
        raise HTTPException(status_code=400, detail="없는 게시물 입니다.")
    except (exception.InvalidPage, exception.InvalidPageLimit):
        raise HTTPException(status_code=400, detail="잘못된 페이지 입니다.")
    else:
        return post


@router.delete(
    "/posts/{post_id}",
    status_code=204,
    response_model=None,
    description="""
- 게시물 삭제\n
- 해당 게시물을 삭제 할 경우 작성된 댓글도 삭제 처리
- 패스워드는 평문으로 받아서 sha256으로 변환 후 기존 패스워드 일치하는지 여부 판단\n
- 패스워드가 일치하지 않는 경우 에러 발생
""",
)
def delete_post(
    post: model.DeletePost, post_id: int, session: Session = Depends(get_session)
):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    try:
        post = service.delete(post_id, post)
    except exception.NotExistPost:
        raise HTTPException(status_code=404, detail="없는 게시물 입니다.")
    else:
        return Response(status_code=204)


@router.get(
    "/posts/{post_id}/comments",
    status_code=200,
    response_model=list[model.ListComment],
    description="""
- 게시물의 댓글 리스트\n
- 순서는 댓글의 id 순이며, 대댓글이 존재 할 시 해당 댓글 다음에 오도록 함\n
- 페이지의 크기는 최대 100까지 가능
""",
)
async def list_comment(
    post_id: int,
    page: int = 1,
    page_limit: int = 10,
    session: Session = Depends(get_session),
):
    repo = repository.CommentRepository(session)
    service = services.CommentService(repo=repo)
    post_repo = repository.PostRepository(session)
    post_service = services.PostService(post_repo)
    try:
        post_service.get(post_id)
        comments = service.get_list(post_id, page, page_limit)
    except (exception.InvalidPage, exception.InvalidPageLimit):
        raise HTTPException(status_code=400, detail="잘못된 페이지 입니다.")
    except exception.NotExistPost:
        raise HTTPException(status_code=400, detail="없는 게시물 입니다.")
    else:
        return comments


@router.post(
    "/posts/{post_id}/comments",
    status_code=201,
    response_model=model.Comment,
    description="""
- 댓글 및 대댓글 작성\n
- 댓글 작성 시에는 parent_id None 또는 key delete\n
- 대댓글 작성 시에는 parent_id에 댓글의 id\n
""",
)
async def create_comment(
    post_id: int, comment: model.CreateComment, session: Session = Depends(get_session)
):
    repo = repository.CommentRepository(session)
    service = services.CommentService(repo)
    try:
        comment = service.add(post_id, comment)
    except exception.NotExistComment:
        raise HTTPException(status_code=400, detail="없는 댓글 입니다.")
    else:
        text = comment.text
        alarm_repo = repository.AlarmRepository(session)
        alram_service = services.AlarmService(alarm_repo, text)
        alram_service.send()
        return comment
