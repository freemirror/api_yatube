from django.shortcuts import get_object_or_404
from posts.models import Group, Post, User
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          UserSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        post_id = self.kwargs.get("pk")
        instance = get_object_or_404(Post, id=post_id)
        if instance.author != self.request.user:
            raise PermissionDenied('Изменять посты других авторов запрещено')
        instance.delete()

    def perform_update(self, serializer):
        post_id = self.kwargs.get("pk")
        post = get_object_or_404(Post, id=post_id)
        if post.author != self.request.user:
            raise PermissionDenied('Изменять посты других авторов запрещено')
        serializer.save()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_destroy(self, instance):
        post_id = self.kwargs.get("post_id")
        comment_id = self.kwargs.get("pk")
        post = get_object_or_404(Post, id=post_id)
        instance = post.comments.get(id=comment_id)
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Изменять коментарии других авторов запрещено'
            )
        instance.delete()

    def perform_update(self, serializer):
        post_id = self.kwargs.get("post_id")
        comment_id = self.kwargs.get("pk")
        post = get_object_or_404(Post, id=post_id)
        comment = post.comments.get(id=comment_id)
        if comment.author != self.request.user:
            raise PermissionDenied(
                'Изменять коментарии других авторов запрещено'
            )
        serializer.save()
