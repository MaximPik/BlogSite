from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, GroupViewSet, UserViewSet, FollowViewSet
from django.urls import path, include
#from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
router.register('groups', GroupViewSet, basename='groups')
router.register('users', UserViewSet, basename='users')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(router.urls)),
    #path('v1/api-token-auth/', views.obtain_auth_token),
    # path('/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
