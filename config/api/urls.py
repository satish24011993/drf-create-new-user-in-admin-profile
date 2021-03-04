from django.conf.urls import url, include
from rest_framework import routers
from api.views import UserViewSet, ProfileAPI, ProfileViewSet, LoginView, ProfileDetail, ProductListAPIView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user/(?P<user_id>\d+)/profile', ProfileAPI, base_name='profile_api')
# router.register(r'profile', ProfileViewSet, base_name='profile')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    # url(r'^user/(?P<user>.+)/profile/$,
    url(r'^profile-list/', ProfileViewSet.as_view(), name='profile'),
    url(r'^profile-list/(?P<pk>\d+)/$', ProfileDetail.as_view(), name='details'),
    url(r'^profile-filter/', ProductListAPIView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/', LoginView.as_view()),
]