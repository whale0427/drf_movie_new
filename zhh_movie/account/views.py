from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated

from account.models import Profile
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from movie.models import Movie
from movie.serializers import MovieSerializer
from utils.error import response_data,MovieError,UserError
from .serializers import ProfileSerializer
from .permissions import ProfilePermission


class CustomPageSizePagination(PageNumberPagination):
    page_size = 14

class CollectViewSet(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    # 因为queryset=Movie.objects.all()在Movie的视图集有了 会造成命名冲突，需要重新定义名称
    basename = "collected_movie"
    serializer_class=MovieSerializer
    pagination_class = CustomPageSizePagination
    permission_classes=[IsAdminUser]

    def get_permissions(self):
        if self.request.method in ["PUT","PATCH"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def list(self,request):
        user=request.user
        profile=Profile.objects.get(user=user)
        movies=profile.movie.all()
        # serializer=MovieSerializer(movies,many=True)

        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(movies, many=True)

        return Response(serializer.data)

    def create(self,request):
        user=request.user
        profile = Profile.objects.get(user=user)
        movie_id=request.data.get("movie_id")
        try:
            movie = Movie.objects.get(pk=movie_id)
            profile.movie.add(movie)
            return Response({"status_code":0,"message":"收藏成功"})
        except ObjectDoesNotExist:
            return Response(response_data(*MovieError.MovieNoFound))
        except:
            return Response({"message":"收藏失败"})

    def destroy(self,request,pk):
        user=request.user
        profile=Profile.objects.get(user=user)
        try:
            movie=Movie.objects.get(pk=pk)
            if movie not in profile.movie.all():
                return Response({"message":"未收藏该电影"})
            profile.movie.remove(movie)
            return Response({"message":"取消收藏成功"})
        except ObjectDoesNotExist:
            return Response({"message":"电影信息不存在"})
        except Exception as e:
            return Response({"message":"取消收藏失败"})

    # @action 是 DRF 提供的装饰器 作用：给视图集添加自定义的端点（endpoint）
    # detail=True：这是一个针对单个对象的动作 对应的 URL 类似：/api/profile/{id}/is_collected/
    # 如果 detail=False：这是针对整个集合的动作 对应的 URL 类似：/api/profile/is_collected/
    # methods=['get']：只允许 GET 请求 也可以允许多个方法：methods=['get', 'post'] 或者使用字符串：methods='get'
    @action(methods=["get"],detail=True)
    def is_collected(self,request,pk):
        user=request.user
        profile=Profile.objects.get(user=user)
        movie=Movie.objects.get(pk=pk)
        is_collected=profile.movie.filter(pk=movie.id).exists()
        return Response({"is_collected":is_collected})

    @action(methods=["get"],detail=False)
    def is_collecteds(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        try:
            movie_ids = profile.movie.values_list("id",flat=True)
            return Response({"movie_ids":movie_ids})
        except ObjectDoesNotExist:
            return Response({"message":"当前用户并无收藏内容"})
        except Exception as e:
            return Response({"message":str(e)})

class ProfileViewSet(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[ProfilePermission]