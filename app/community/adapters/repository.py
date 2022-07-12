import abc

from app.community.adapters import orm
from app.community.domain import model
from sqlalchemy import types
from sqlalchemy.sql.expression import cast, text
from sqlalchemy.sql.functions import concat


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
        if q:
            query = query.filter(
                (orm.Post.user_name.like(f"%{q}%")) | orm.Post.title.like(f"%{q}%")
            )
        if page_limit:
            query = query.limit(page_limit)
        if page:
            query = query.offset((page - 1) * page_limit)
        return query.all()

    def add(self, post: model.CreatePost) -> orm.Post:
        db_post = orm.Post(**post.dict())
        self.session.add(db_post)
        self.session.commit()
        self.session.refresh(db_post)
        return db_post

    def update(self, post_id: int, post: model.UpdatePost):
        self.session.query(orm.Post).filter(orm.Post.id == post_id).update(
            post.dict(exclude=["password"])
        )
        self.session.commit()
        return self.get(post_id)

    def delete(self, post_id: int):
        self.session.query(orm.Post).filter(orm.Post.id == post_id).delete()
        self.session.commit()
        return None


class CommentRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, post_id, depth, comment: orm.Comment):
        db_comment = orm.Comment(**comment.dict())
        db_comment.post_id = post_id
        db_comment.depth = depth
        self.session.add(db_comment)
        self.session.commit()
        self.session.refresh(db_comment)
        return db_comment

    def get(self, comment_id) -> orm.Comment:
        query = self.session.query(orm.Comment).filter_by(id=comment_id).first()
        return query

    def get_list(self, post_id, page, page_limit) -> list[orm.Comment]:
        query = (
            self.session.query(
                orm.Comment,
                cast(orm.Comment.id.label("path"), types.CHAR(1000)),
            )
            .filter(orm.Comment.post_id == post_id)
            .cte("cte", recursive=True)
        )
        re_query = self.session.query(
            orm.Comment,
            concat(query.c.path, ",", cast(orm.Comment.id, types.CHAR(1000))).label(
                "path"
            ),
        )
        re_query = re_query.join(query, orm.Comment.parent_id == query.c.id)
        recursive_q = query.union(re_query)
        q = self.session.query(recursive_q)
        q = q.order_by(text("path+1"), "path")
        if page_limit:
            q = q.limit(page_limit)
        if page:
            q = q.offset((page - 1) * page_limit)
        return q.all()
