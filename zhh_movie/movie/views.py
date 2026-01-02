from django.http import JsonResponse, Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.views import APIView
from django_filters import rest_framework as filters

from .models import Movie, Category
# from .serializers import MovieListSerializer,MovieDetailSerializer
from .serializers import MovieSerializer,CategorySerializer
from .permissions import IsAdminUserOrReadOnly

# Create your views here.
# @api_view(["GET","POST"])
# def movie_list(request):
#     if request.method=="GET":
#         movies=Movie.objects.all()
#         serializer=MovieListSerializer(movies,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     elif request.method=="POST":
#         serializer=MovieListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#第一种方式：使用视图APIView
# class MovieDetail(APIView):
#     def get(self,request,pk):
#         try :
#             movie=Movie.objects.get(pk=pk)
#         except:
#             raise Http404
#         serializer=MovieDetailSerializer(movie)
#         return Response(serializer.data)
#
#     def put(self,request,pk):
#         try :
#             movie=Movie.objects.get(pk=pk)
#         except:
#             raise Http404
#         serializer=MovieDetailSerializer(movie,data=request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,request,pk):
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except:
#             raise Http404
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#第二种方式：使用通用视图generics.GenericAPIView
# class MovieDetail(mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   generics.GenericAPIView):
#     queryset=Movie.objects.all()
#     serializer_class=MovieDetailSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
#
#     def put(self,request,*args,**kwargs):
#         return self.partial_update(request,*args,**kwargs)
#
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)
#第二种方式的更简易写法：使用通用视图，自行查看generics类里面自带更简易的视图类。如下面例子
# class MovieList(generics.ListAPIView):
#     queryset = Movie.objects.all()
#     serializer_class=MovieListSerializer
# class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Movie.objects.all()
#     serializer_class=MovieDetailSerializer
#################
class MovieFilter(filters.FilterSet):
    # icontains 不区分大小写的模糊查询，i不区分大小写 contains包含在内
    movie_name=filters.CharFilter(field_name='movie_name',lookup_expr='icontains')
    # 精确查找，就不用写lookup_expr，会默认exact：精确匹配
    category=filters.NumberFilter(field_name='category')
    class Meta:
        model=Movie
        fields=["movie_name","category","region"]
#也可以缩减内容
# class MovieFilter(filters.FilterSet):
#     # icontains 不区分大小写的模糊查询，i不区分大小写 contains包含在内
#     movie_name=filters.CharFilter(field_name='movie_name',lookup_expr='icontains')
#     #category可以用默认的  意思是当Meta里面有fields  那么Django Filter 会自动为字段创建默认过滤器
#     #默认是精确匹配，所以category=filters.NumberFilter(field_name='category')可以不用写
#     class Meta:
#         model=Movie
#         fields=["movie_name","category"]
#################
#第三种方式：视图集viewsets.ModelViewSet，里面带有上面两种方式的所有内容
class MovieViewSet(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields=("movie_name",)
    filterset_class=MovieFilter
    permission_classes = [IsAdminUserOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

