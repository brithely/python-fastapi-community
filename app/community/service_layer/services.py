from datetime import datetime

from app.community.adapters.repository import (
    AlarmRepository,
    CommentRepository,
    PostRepository,
)
from app.community.domain import exception, model


def validate_page(page, page_limit):
    if page < 1:
        raise exception.InvalidPage
    if page_limit < 1 or page_limit > 100:
        raise exception.InvalidPageLimit
    return True


def check_password(password1, password2):
    if password1 != password2:
        raise exception.InvalidPassword
    return True


class PostService:
    def __init__(self, repo: PostRepository):
        self._repo = repo

    def get(self, post_id):
        post = self._repo.get(post_id)
        if not post:
            raise exception.NotExistPost
        return post

    def get_list(self, q, page, page_limit):
        """
        page: 1 이상으로 음수일 경우 에러
        page_limit: 1 이상으로 음수일 경우 에러
        """
        validate_page(page, page_limit)
        return self._repo.get_list(q, page, page_limit)

    def add(self, post: model.CreatePost):
        return self._repo.add(post)

    def update(self, post_id, post: model.UpdatePost):
        exist_post = self._repo.get(post_id)
        if not exist_post:
            raise exception.NotExistPost
        check_password(exist_post.password, post.password)
        post.updated_at = datetime.now()
        return self._repo.update(post_id, post)

    def delete(self, post_id, post: model.DeletePost):
        exist_post = self._repo.get(post_id)
        if not exist_post:
            raise exception.NotExistPost
        check_password(exist_post.password, post.password)
        return self._repo.delete(post_id)


class CommentService:
    def __init__(self, repo: CommentRepository):
        self._repo = repo

    def get(self, comment_id):
        return self._repo.get(comment_id)

    def get_list(self, post_id, page, page_limit):
        """
        page: 1 이상으로 음수일 경우 에러
        page_limit: 1 이상으로 음수일 경우 에러
        """
        validate_page(page, page_limit)
        return self._repo.get_list(post_id, page, page_limit)

    def add(self, post_id, comment: model.CreateComment):
        """
        depth의 경우 하위 코멘트인 경우 부모 코멘트의 depth를 가져와서 +1
        """
        if comment.parent_id:
            parent_comment = self.get(comment.parent_id)
            depth = parent_comment.depth + 1
        else:
            depth = 1
        return self._repo.add(post_id, depth, comment)


class AlarmService:
    def __init__(self, repo: AlarmRepository, text):
        self._text = text
        self._repo = repo

    def _get_keyword_id_list(self):
        keyword_list = self._parsing_keywords_from_text()
        return self._repo.get_list_keyword_id_by_keyword_list(keyword_list)

    def _get_attended_alram_author_id_list(self, keyword_id_list):
        return self._repo.get_list_author_id_by_keyword_id_list(keyword_id_list)

    def _parsing_keywords_from_text(self) -> list[str]:
        parsed_keywords = self._text.split()
        return parsed_keywords

    def _send_alarm_to_author_id_list(self, author_id_list):
        """
        중복 제거
        실제로 푸시가 나가는 로직
        """
        author_id_list = set(author_id_list)
        for author_id in author_id_list:
            print(f"send alarm {author_id} done")
        return True

    def send(self):
        keyword_id_list = self._get_keyword_id_list()
        author_id_list = self._get_attended_alram_author_id_list(keyword_id_list)
        return self._send_alarm_to_author_id_list(author_id_list)
