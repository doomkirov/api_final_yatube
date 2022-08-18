from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet


app_name = 'api'
router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='posts')
router_v1.register(r'groups', GroupViewSet, basename='groups')
router_v1.register(
    r'posts/(?P<post_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/follow/', FollowViewSet.as_view()),
    path('v1/', include('djoser.urls.jwt')),
]
