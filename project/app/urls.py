from django.urls import path, include
from rest_framework import routers

from .views import ProductViewSet, LessonViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('lessons', LessonViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]