from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, AllowAny, )
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from authors.apps.article_tags.views import ArticleTagView
from authors.apps.article_tags.models import ArticleTag
from .article_filter import ArticleFilter
from .renderer import ArticleJSONRenderer
from .models import Article, Like_Dislike, Report
from .serializers import ArticleSerializer, ReportSerializer,\
    UserReadsSerializer, ReadingStatsSerializer
from .permissions import IsOwnerOrReadOnly
from .pagination import ArticlePageNumberPagination
from .readtime_engine import ArticleTimeEngine
from drf_yasg.utils import swagger_auto_schema
from .reading_stats import UserReads, UserViews
import datetime


class ListArticles(generics.ListAPIView):
    """ Get articles"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = ()
    renderer_classes = (ArticleJSONRenderer, )
    pagination_class = ArticlePageNumberPagination

    filter_class = ArticleFilter
    filter_backends = (SearchFilter, DjangoFilterBackend, )
    search_fields = ('title', 'author__username', 'description',)


class CreateArticles(generics.CreateAPIView):
    """
    POST articles/
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ArticleJSONRenderer, )
    pagination_class = ArticlePageNumberPagination

    def create(self, request, **kwargs):
        data = {}
        data["title"] = request.data.get("title")
        data["description"] = request.data.get("description")
        data["body"] = request.data.get("body")
        data["tagList"] = request.data.get("tagList")
        ArticleTagView.create_tag(ArticleTagView, request.data.get("tagList"))
        serializer = ArticleSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        read_time = ArticleTimeEngine(data['body'])
        save_serialiser = serializer.save(
            author=self.request.user,
            read_time=read_time.read_time()
        )
        for tag in data['tagList']:
            save_serialiser.tagList.add(
                ArticleTag.objects.get(article_tag_text=tag))
        return Response({"article": serializer.data}, status=status.HTTP_201_CREATED)


class RetrieveArticle(APIView):
    """
    GET articles/:id/
    """
    queryset = Article.objects.all()
    authentication_classes = ()
    serializer_class = ArticleSerializer
    err_message = {"errors": "That article is not found"}

    def get(self, request, pk, **kwargs):
        user = request.user
        queryset = Article.objects.all().filter(id=pk)
        if queryset:
            serializer = ArticleSerializer(
                queryset, many=True, context={'request': request})
            return Response(serializer.data)
        return Response(self.err_message, status=status.HTTP_404_NOT_FOUND)


class UpdateDestroyArticle(generics.RetrieveUpdateDestroyAPIView):
    """
    PUT articles/:id/
    DELETE articles/:id/
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    renderer_classes = (ArticleJSONRenderer, )
    err_message = {"errors": "That article is not found"}

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        tags = request.data.get("tagList")
        tag = ArticleTagView.create_tag(
            ArticleTagView, request.data.get("tagList"))
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if not tags:
            instance.tagList.clear()
        for tag in tags:
            get_tag = ArticleTag.objects.all()
            for remove_tag in get_tag:
                if str(remove_tag) not in tags:
                    instance.tagList.remove(remove_tag)
            instance.tagList.add(
                ArticleTag.objects.get(article_tag_text=tag))
        return Response(serializer.data)

    def destroy(self, request, pk, **kwargs):
        user = request.user
        queryset = Article.objects.all().filter(id=pk)
        if queryset:
            if queryset[0].author == user:
                self.perform_destroy(queryset)
                return Response("You have succesfully deleted the article")
            return Response("You do not have permision to delete the article")
        return Response(self.err_message, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        """
        Method for getting an article and adding a view
        """
        instance = self.get_object()
        user = request.user
        try:
            view = UserViews.objects.get(user=user.id, article=instance.id)
        except:
            if instance.author.id != user.id:
                view = UserViews(user=user, article=instance)
                view.save()
                view = UserViews.objects.all()
        return self.retrieve(request, *args, **kwargs)


class Like(APIView):
    """
    POST articles/:id/like/ to like an article
    GET articles/:id/ and view likes_count
    """
    permission_classes = (IsAuthenticated, )

    def get_article(self, article_id):
        """ Method to search for an article object by its id"""
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFound({"error": "Article does not exist"})

    def post(self, request, **kwargs):
        """ Method to like an article """

        article = self.get_article(kwargs['article_id'])

        my_choice = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username)
        my_choice_reset = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=0)
        my_like_already = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=1)
        my_dislike_already = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=-1)

        if not my_choice:
            like = Like_Dislike(
                reviewer=request.user, like_or_dislike=1, article=article
            )
            like.save()
            Article.objects.filter(
                id=kwargs['article_id']).update(
                likes_count=article.likes_count + 1)
            return Response({"success": "You have successfully liked this article."})
        else:
            if my_choice_reset:
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'],
                    reviewer_id=request.user.username).update(like_or_dislike=1)
                Article.objects.filter(
                    id=kwargs['article_id']).update(
                    likes_count=article.likes_count + 1)
                return Response({"success": "You have successfully liked this article."})
            elif my_like_already:
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).update(like_or_dislike=0)
                Article.objects.filter(
                    id=kwargs['article_id']).update(likes_count=article.likes_count - 1)
                return Response(
                    {"message": "Your like has been revoked"}, status=status.HTTP_200_OK,)
            elif my_dislike_already:
                like_dislike = Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).first()
                like_dislike.like_or_dislike = 1
                like_dislike.save()
                Article.objects.filter(
                    id=kwargs['article_id']).update(
                        likes_count=article.likes_count + 1, dislikes_count=article.dislikes_count - 1)
                return Response({"success": "Your dislike for the article has changed to a like."})


class Dislike(APIView):
    """
    POST articles/:id/dislike/ to dislike an article
    GET articles/:id/ and view dislikes_count
    """
    permission_classes = (IsAuthenticated, )

    def get_article(self, article_id):
        """ Method to search for an article object by its id"""
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFound({"error": "Article does not exist"})

    def post(self, request, **kwargs):
        """ Method to dislike an article """
        article = self.get_article(kwargs['article_id'])
        my_choice = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username)
        my_choice_reset = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=0)
        my_dislike_already = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=-1)
        my_like_already = Like_Dislike.objects.filter(
            article_id=kwargs['article_id'], reviewer_id=request.user.username, like_or_dislike=1)
        if not my_choice:
            dislike = Like_Dislike(
                reviewer=request.user, like_or_dislike=-1, article=article)
            dislike.save()
            Article.objects.filter(
                id=kwargs['article_id']).update(
                    dislikes_count=article.dislikes_count + 1)
            return Response({"success": "You have successfully disliked this article."})
        else:
            if my_choice_reset:
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).update(like_or_dislike=-1)
                Article.objects.filter(
                    id=kwargs['article_id']).update(
                        dislikes_count=article.dislikes_count + 1)
                return Response({"success": "You have successfully disliked this article."})
            elif my_dislike_already:
                Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).update(like_or_dislike=0)
                Article.objects.filter(
                    id=kwargs['article_id']).update(dislikes_count=article.dislikes_count - 1)
                return Response(
                    {"message": "Your dislike has been revoked"}, status=status.HTTP_200_OK,)
            elif my_like_already:
                like_dislike = Like_Dislike.objects.filter(
                    article_id=kwargs['article_id'], reviewer_id=request.user.username).first()
                like_dislike.like_or_dislike = -1
                like_dislike.save()
                Article.objects.filter(
                    id=kwargs['article_id']).update(
                        likes_count=article.likes_count - 1, dislikes_count=article.dislikes_count + 1)
                return Response({"success": "Your like for the article has changed to a dislike."})


class Reports(APIView):
    """POST articles/:id/report/ to report an article"""
    permission_classes = (IsAuthenticated, )
    serializer_class = ReportSerializer

    def get_article_object(self, article_id):
        """ Method to search for an article object by its id"""
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFound({"error": "Article does not exist"})

    def get_report_object(self, article_id, username):
        """ Method to search for a report by the article id and username """
        try:
            return Report.objects.get(article=article_id, reporter_id=username)
        except Report.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Report an article.",
        operation_id="Report an article.",
        request_body=serializer_class,
        responses={200: serializer_class(many=False), 400: "BAD REQUEST"},
    )
    def post(self, request, **kwargs):
        """ Method to post a report"""
        article = self.get_article_object(kwargs['article_id'])
        report = self.get_report_object(
            kwargs['article_id'], request.user.username)
        if report:
            return Response({"error": "You already reported this article"})
        else:
            report = request.data.get("report", {})
            report['reporter'] = request.user.username
            report['date_reported'] = timezone.now()
            report['article'] = article.id
            serializer = ReportSerializer(data=report)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            Article.objects.filter(
                id=kwargs['article_id']).update(report_count=article.report_count + 1, reported=True)
            return Response({
                "report": serializer.data,
                "message": "Report successfully created."
            }, status=status.HTTP_201_CREATED)


class ReportView(APIView):
    """ GET articles/report/ to view all reports """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """ To get all reports of articles """
        if request.user.is_superuser:
            reported = []
            reports = Report.objects.all()
            report = ReportSerializer(reports, many=True)
            reported.append(report.data)
            return Response({
                "reports": reported}, status.HTTP_200_OK)
        return Response(
            {"error": "You do not have permission to view the reported articles"},
            status.HTTP_403_FORBIDDEN)


class AddRead(generics.CreateAPIView):
    """
    View class for registering a user read
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserReadsSerializer

    def create(self, request, **kwargs):
        """
        Method for adding a user read
        """
        user = request.user
        article_id = request.data.get('article_id')
        if not article_id:
            return Response({'error': 'You must provide an article id to proceed'},
                            status.HTTP_400_BAD_REQUEST)
        try:
            read = UserReads.objects.get(article=article_id, user=user.id)
            if read:
                return Response({"message": "User read exists"},
                                status.HTTP_400_BAD_REQUEST)
        except:
            try:
                article = Article.objects.get(id=article_id)
                if article.author.id != user.id:
                    read = UserReads(user=user, article=article)
                    read.save()
                    return Response({'message': "User read recorded"},
                                    status.HTTP_201_CREATED)
            except:
                return Response({'error': 'Article doesnot exist'},
                                status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Author can not read their own article'},
                        status.HTTP_400_BAD_REQUEST)


class ReadingStats(generics.RetrieveAPIView):
    """
    View class user reading statistics
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ReadingStatsSerializer

    def read_ratio(self, reads, views):
        """
        Method computes the read ratio of an article
        """
        try:
            ratio = (reads/views)*100
            return round(ratio)
        except:
            return 0

    def stats_in_last_30_days(self, obj, today, days, viewed, stats_for):
        """
        method to return records the were recorded in the past 30 days
        """
        days = datetime.timedelta(days=days)
        start_date = today - days
        if stats_for == "views":
            return obj.objects.filter(
                viewed_on__range=(start_date, today), article=viewed)
        elif stats_for == "reads":
            return obj.objects.filter(
                read_on__range=(start_date, today), article=viewed)
        elif stats_for == "likes":
            return obj.objects.filter(
                date_liked__range=(start_date, today), article=viewed,
                like_or_dislike=1)
        elif stats_for == "dislikes":
            return obj.objects.filter(
                date_liked__range=(start_date, today), article=viewed,
                like_or_dislike=-1)

    def total_views(self, article):
        """
        Method returns total number of views for an article
        """
        len_of_views = len(UserViews.objects.filter(article=article.id))
        return len_of_views

    def total_reads(self, article):
        """
        Method returns the total number of reads for an 
        article
        """
        len_of_reads = len(UserReads.objects.filter(article=article.id))
        return len_of_reads

    def views_30_days(self, article, today):
        """
        Method returns the number of views in the last 30 days
        """
        views = len(self.stats_in_last_30_days(
            UserViews, today, 30, article.id, 'views'
        ))
        return views

    def reads_30_days(self, article, today):
        """
        Method returns the number of reads in the last 30 days
        """
        reads = len(self.stats_in_last_30_days(
                    UserReads, today, 30, article.id, 'reads'))
        return reads

    def likes_30_days(self, article, today):
        """
        Method returns the number of likes in last 30 days
        """
        likes = len(self.stats_in_last_30_days(Like_Dislike,
                                               today, 30, article.id, 'likes'
                                               ))
        return likes

    def dislikes_30_days(self, article, today):
        """
        Method returns the number of dislikes in the last 
        30 days
        """
        dislikes = len(self.stats_in_last_30_days(Like_Dislike,
                                                  today, 30, article.id, 'dislikes'
                                                  ))
        return dislikes

    def get(self, request, *args, **kwargs):
        """
        Method gets statistics for reading stats for an 
        author's articles
        """
        # compute article statistics
        article_list = []
        today = datetime.datetime.now()
        user_articles = Article.objects.filter(author=request.user)
        for user_article in user_articles:
            viewed_articles = UserViews.objects.filter(
                article=user_article.id)
            article_list.append({'article_id': user_article.id,
                                 'article_title': user_article.title,
                                 'total_views': self.total_views(
                                     user_article
                                 ),
                                 'total_reads': self.total_reads(
                                     user_article
                                 ),
                                 'read_ratio': self.read_ratio(
                                     len(UserReads.objects.filter(
                                         article=user_article.id
                                     )),
                                     len(UserViews.objects.filter(
                                         article=user_article.id
                                     ))),
                                 'views_in_last_30_days': self.views_30_days(
                                     user_article, today
                                 ),
                                 'reads_in_last_30_days': self.reads_30_days(
                                     user_article, today
                                 ),
                                 'likes_in_last_30_days': self.likes_30_days(
                                     user_article, today
                                 ),
                                 'dislikes_in_last_30_days': self.dislikes_30_days(
                                     user_article, today
                                 )})
        return Response({"reading_statistics": article_list})
