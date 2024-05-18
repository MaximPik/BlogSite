from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from posts.models import Post, Group, User, Follow
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, UserSerializer, FollowSerializer, FollowListSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.exceptions import NotFound



class PostViewSet(viewsets.ModelViewSet):
    # показывает, какой сериализатор используем
    serializer_class = PostSerializer
    # правила доступа:
    # IsAuthenticatedOrReadOnly - Get запросы могут делать все, а RUD запросы - только авторезированные пользователи
    # IsOwnerOrReadOnly - изменяет или удаляет пост только автор
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get_queryset(self):
        # queryset указывает, какие объекты модели будут доступны
        queryset = Post.objects.all()
        group_id = self.request.query_params.get('group')
        if group_id is not None:
            try:
                queryset = queryset.filter(group_id=group_id)
            except Group.DoesNotExist:
                raise NotFound(detail=f"Группа с ID {group_id} не найдена.")
        return queryset

    # функция для создания нового поста
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    
    # Этот класс переопределён, чтобы получать не все посты, а только те,
    # которые прикреплены к указанному id поста
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()
    
    # Создание нового комментария
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        print(post)
        serializer.save(author=self.request.user, post=post)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def list(self, request):
        following = Follow.objects.filter(user=request.user)
        followers = Follow.objects.filter(author=request.user)
        serializer = FollowListSerializer({'following': following, 'followers': followers})
        return Response(serializer.data)
    
    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)