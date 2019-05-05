from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import ArticleTag
from .serializers import ArticleTagSerializer


class ArticleTagView(ModelViewSet):
    """
    View class for Article tag
    """
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer


    def create_tag(self, tags):
        if tags:
            for tag in tags:
                try:
                    ArticleTag.objects.get(article_tag_text=tag)
                except ObjectDoesNotExist:
                    data = {'article_tag_text': tag}
                    serializer = ArticleTagSerializer(data=data)
                    serializer.is_valid()
                    self.perform_create(ArticleTagView, serializer)
