from app.community.adapters.repository import CommentRepository, PostRepository
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
        # TODO: Added Alarm Logic
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
        if page < 1:
            raise ValueError("잘못된 페이지")
        if page_limit < 1:
            raise ValueError("잘못된 페이지 크기")
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
