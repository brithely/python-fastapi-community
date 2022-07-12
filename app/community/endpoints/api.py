from typing import Union

from app.community.adapters import repository
from app.community.database import get_session
from app.community.domain import model
from app.community.service_layer import services
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/posts", status_code=200, response_model=list[model.Post])
async def list_post(
    page: int = 1,
    page_limit: int = 10,
    q: Union[str, None] = None,
    session: Session = Depends(get_session),
):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    return service.get_list(q=q, page=page, page_limit=page_limit)


@router.post("/posts", status_code=201, response_model=model.Post)
async def create_post(post: model.CreatePost, session: Session = Depends(get_session)):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    try:
        post = service.add(post)
    except Exception:
        raise
    else:
        return post
    finally:
        text = " ".join([post.title, post.text])
        alarm_repo = repository.AlarmRepository(session)
        alram_service = services.AlarmService(alarm_repo, text)
        alram_service.send()


@router.put("/posts/{post_id}", status_code=201, response_model=model.Post)
def update_post(
    post: model.UpdatePost, post_id: int, session: Session = Depends(get_session)
):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    return service.update(post_id, post)


@router.delete("/posts/{post_id}", status_code=204, response_model=None)
def delete_post(
    post: model.DeletePost, post_id: int, session: Session = Depends(get_session)
):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    return service.delete(post_id, post)


@router.get(
    "/posts/{post_id}/comments", status_code=200, response_model=list[model.ListComment]
)
async def list_comment(
    post_id: int,
    page: int = 1,
    page_limit: int = 10,
    session: Session = Depends(get_session),
):
    repo = repository.CommentRepository(session)
    service = services.CommentService(repo=repo)
    return service.get_list(post_id, page, page_limit)


@router.post("/posts/{post_id}/comments", status_code=201, response_model=model.Comment)
async def create_comment(
    post_id: int, comment: model.CreateComment, session: Session = Depends(get_session)
):
    repo = repository.CommentRepository(session)
    service = services.CommentService(repo)
    try:
        comment = service.add(post_id, comment)
    except Exception:
        raise
    else:
        return comment
    finally:
        text = comment.text
        alarm_repo = repository.AlarmRepository(session)
        alram_service = services.AlarmService(alarm_repo, text)
        alram_service.send()
