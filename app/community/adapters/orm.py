from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

Base = declarative_base()
metadata = Base.metadata


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    text = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    password = Column(String(256))
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author", backref=backref("posts", order_by=id))


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    post = relationship("Post", backref=backref("comments", order_by=id))
    parent_id = Column(Integer, ForeignKey("comment.id"))
    parent = relationship(
        "Comment", backref=backref("replies", order_by=id), remote_side=[id]
    )
    depth = Column(Integer, default=1, nullable=False)
    text = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author", backref=backref("comments", order_by=id))


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)


class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(1000), nullable=False)


class AuthorKeyword(Base):
    __tablename__ = "author_keyword"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    author = relationship("Author", backref=backref("keywords", order_by=id))
    keyword_id = Column(Integer, ForeignKey("keyword.id"), nullable=False)
    keyword = relationship("Keyword", backref=backref("authors", order_by=id))
