from django.conf.urls import include
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
