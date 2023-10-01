from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, Lesson, UserProfile
from .serializers import ProductSerializer, LessonSerializer, StatisticSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    """Получение статистики с методом GET по адресу: http://127.0.0.1:8000/api/products/statistics/"""

    @action(detail=False, methods=['get'], url_path="statistics")
    def get_statistics(self, request, pk=None):
        products = Product.objects.all()
        serializer = StatisticSerializer(products, many=True)
        result = serializer.data
        return Response(result)


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    """Доступ к списку всех уроков по всем продуктам с методом POST и телом запроса {user_id: Номер} 
    по адресу http://127.0.0.1:8000/api/lessons/all-users-lessons/"""

    @action(detail=False, methods=['post'], url_path="all-users-lessons")
    def get_all_lessons(self, request, pk=None):
        user = UserProfile.objects.get(id=request.data["user_id"])
        products = Product.objects.filter(access__user_id=user.id, access__is_granted=True)
        queryset = Lesson.objects.filter(product__in=products)
        serializer = LessonSerializer(queryset, many=True, context={"data": request.data})
        result = serializer.data

        for i in result:
            del i['watched_at']

        return Response(result)

    """Доступ к списка уроков по конкретному продукту с методом POST и телом запроса
     {user_id: Номер, "product_id":Номер } по адресу http://127.0.0.1:8000/api/lessons/definite-users-lessons/"""

    @action(detail=False, methods=['post'], url_path="definite-users-lessons")
    def get_definite_lessons(self, request, pk=None):
        user = UserProfile.objects.get(id=request.data["user_id"])
        products = Product.objects.filter(access__user_id=user.id, access__is_granted=True,
                                          id=request.data["product_id"])
        queryset = Lesson.objects.filter(product__in=products)
        serializer = LessonSerializer(queryset, many=True, context={"data": request.data})
        result = serializer.data
        return Response(result)
