# TODO:  Напишите свой вариант
from sqlite3 import IntegrityError
from rest_framework import viewsets, permissions, serializers
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Follow, User
from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
from .permissions import IsAbleToFolow, IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated & IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated & IsAbleToFolow]

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        try:
            serializer.save(
                user=self.request.user,
                author=User.objects.get(username=self.request.data['author'])
            )
        except Exception:
            return IntegrityError(
                'Нельзя подписаться на одного пользователя дважды!'
            )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated & IsAuthorOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )

    def get_queryset(self):
        return self.get_post().comments.all()
