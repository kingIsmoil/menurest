from django.urls import path
from .views import RegisterView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,LogoutView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
