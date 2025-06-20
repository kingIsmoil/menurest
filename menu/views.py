from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Foods, Order,models
from .serializers import FoodsSerializer, OrderSerializer
from .permissions import IsAdminOrReadOnly, IsOrderOwnerOrAdmin


class FoodsViewSet(viewsets.ModelViewSet):
    queryset = Foods.objects.all().order_by('name')
    serializer_class = FoodsSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['name', 'price']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
            
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset.distinct()

    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular_foods = Foods.objects.annotate(
            order_count=models.Count('order')
        ).order_by('-order_count')[:5]
        serializer = self.get_serializer(popular_foods, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOrderOwnerOrAdmin]
    
    def get_queryset(self):
        queryset = Order.objects.select_related('user', 'food')
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
            
        is_active = self.request.query_params.get('is_active')
        if is_active:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if not order.is_active:
            return Response(
                {'error': 'Заказ уже отменен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.is_active = False
        order.save()
        return Response({'status': 'Заказ отменен'})

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)