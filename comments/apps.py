from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = 'comments'

    def ready(self):
        import comments.signals