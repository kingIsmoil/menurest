from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodsViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'foods', FoodsViewSet, basename='foods')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]