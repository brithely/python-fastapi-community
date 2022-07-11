from typing import Union

from app.community.adapters import repository
from app.community.database import get_session
from app.community.domain import model
from app.community.service_layer import services
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/posts", status_code=200, response_model=list[model.Post])
async def list_post(page: int = 1, page_limit: int = 10, q: Union[str, None] = None, session: Session = Depends(get_session)):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    return service.get_list(q=q, page=page, page_limit=page_limit)


@router.post("/posts", status_code=201, response_model=model.Post)
async def create_post(post: model.CreatePost, session: Session = Depends(get_session)):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    return service.add(post)


@router.put("/posts/{post_id}", status_code=201, response_model=model.Post)
def update_post(post: model.UpdatePost, post_id: int, session: Session = Depends(get_session)):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    return service.update(post_id, post)


@router.delete("/posts/{post_id}", status_code=204, response_model=None)
def delete_post(post: model.DeletePost, post_id: int, session: Session = Depends(get_session)):
    repo = repository.PostRepository(session)
    service = services.PostService(repo=repo)
    return service.delete(post_id, post)

