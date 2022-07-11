import abc

from app.community.adapters import orm
from app.community.domain import model


class AbstractRepository(abc.ABC):
    pass


class PostRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get(self, post_id: int) -> orm.Post:
        query = self.session.query(orm.Post).filter_by(id=post_id).first()
        return query

    def get_list(self, q, page, page_limit) -> list[orm.Post]:
        query = self.session.query(orm.Post)
        if q: query = query.filter((orm.Post.user_name.like(f"%{q}%"))|orm.Post.title.like(f"%{q}%"))
        if page_limit: query = query.limit(page_limit)
        if page: query = query.offset((page-1)*page_limit)
        return query.all()
        
    def add(self, post: model.CreatePost) -> orm.Post:
        db_post = orm.Post(**post.dict())
        self.session.add(db_post)
        self.session.commit()
        self.session.refresh(db_post)
        return db_post

    def update(self, post_id: int, post: model.UpdatePost):
        self.session.query(orm.Post).filter(orm.Post.id==post_id).update(post.dict())
        self.session.commit()
        return self.get(post_id)

    def delete(self, post_id: int):
        self.session.query(orm.Post).filter(orm.Post.id==post_id).delete()
        self.session.commit()
        return None


class CommentRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
        
    def add(self, post: model.Post):
        raise NotImplementedError

    def get(self, post_id) -> model.Post:
        raise NotImplementedError

    def get_posts(self) -> model.Post:
        return self.session.query(orm.Post).all()
