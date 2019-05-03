from rest_framework.pagination import PageNumberPagination


class ArticlePageNumberPagination(PageNumberPagination):
    """
    This Django pagination style accepts a single number
    page number in the request query parameters.
    """
    page_size = 10
