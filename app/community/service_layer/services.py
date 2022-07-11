from app.community.adapters.repository import PostRepository
from app.community.domain import model


class PostService:
    def __init__(self, repo: PostRepository):
        self._repo = repo

    def get(self, post_id):
        return self._repo.get(post_id)

    def get_list(self, q, page, page_limit):
        """
            page: 1 이상으로 음수일 경우 에러
            page_limit: 1 이상으로 음수일 경우 에러
        """
        if page < 1:
            raise ValueError("잘못된 페이지")
        if page_limit < 1:
            raise ValueError("잘못된 페이지 크기")
        return self._repo.get_list(q, page, page_limit)

    def add(self, post: model.CreatePost):
        return self._repo.add(post)

    def update(self, post_id, post: model.UpdatePost):
        exist_post = self._repo.get(post_id)
        if not exist_post:
            raise ValueError("없는 게시물")
        if exist_post.password != post.password:
            raise ValueError("잘못된 패스워드")
        return self._repo.update(post_id, post)

    def delete(self, post_id, post: model.DeletePost):
        exist_post = self._repo.get(post_id)
        if not exist_post:
            raise ValueError("없는 게시물")
        if exist_post.password != post.password:
            raise ValueError("잘못된 패스워드")
        return self._repo.delete(post_id)
