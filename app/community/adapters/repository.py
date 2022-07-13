import abc
from datetime import datetime

from app.community.adapters import orm
from app.community.domain import model
from sqlalchemy import or_, types
from sqlalchemy.sql.expression import cast, text
from sqlalchemy.sql.functions import concat


class AbstractRepository(abc.ABC):
    pass


class AuthorMixin:
    def get_or_update_author(self, user_name: str) -> orm.Author:
        instance = (
            self.session.query(orm.Author).filter(orm.Author.name == user_name).first()
        )
        if instance:
            return instance
        else:
            instance = orm.Author(**{"name": user_name})
            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance)
            return instance


class PostRepository(AuthorMixin, AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get(self, post_id: int) -> orm.Post:
        query = (
            self.session.query(orm.Post)
            .filter_by(id=post_id)
            .join(orm.Post.author)
            .first()
        )
        return query

    def get_list(self, q, page, page_limit) -> list[orm.Post]:
        query = self.session.query(orm.Post).join(orm.Post.author)
        if q:
            query = query.filter(
                (orm.Author.name.like(f"%{q}%")) | orm.Post.title.like(f"%{q}%")
            )
        if page_limit:
            query = query.limit(page_limit)
        if page:
            query = query.offset((page - 1) * page_limit)
        return query.all()

    def add(self, post: model.CreatePost) -> orm.Post:
        author = self.get_or_update_author(post.author)
        db_post = orm.Post(**post.dict(exclude={"author"}))
        db_post.author_id = author.id
        self.session.add(db_post)
        self.session.commit()
        self.session.refresh(db_post)
        return db_post

    def update(self, post_id: int, post: model.UpdatePost):
        self.session.query(orm.Post).filter(orm.Post.id == post_id).update(
            post.dict(exclude={"password", "created_at"})
        )
        self.session.commit()
        return self.get(post_id)

    def delete(self, post_id: int):
        self.session.query(orm.Comment).filter(orm.Comment.post_id == post_id).delete()
        self.session.query(orm.Post).filter(orm.Post.id == post_id).delete()
        self.session.commit()
        return None


class CommentRepository(AuthorMixin, AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, post_id, depth, comment: model.Comment):
        author = self.get_or_update_author(comment.author)
        db_comment = orm.Comment(**comment.dict(exclude={"author"}))
        db_comment.post_id = post_id
        db_comment.depth = depth
        db_comment.author_id = author.id
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


class AlarmRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get_list_keyword_id_by_keyword_list(self, keyword_list: list) -> list[int]:
        query = self.session.query(orm.Keyword)
        q = []
        for keyword in keyword_list:
            q.append(orm.Keyword.text == keyword)
        query = query.filter(or_(*q))
        return [r[0] for r in query.values(orm.Keyword.id)]

    def get_list_author_id_by_keyword_id_list(self, keyword_id_list: list) -> list[int]:
        query = self.session.query(orm.AuthorKeyword)
        query = query.filter(orm.AuthorKeyword.keyword_id.in_(keyword_id_list))
        return [r[0] for r in query.values(orm.AuthorKeyword.author_id)]
