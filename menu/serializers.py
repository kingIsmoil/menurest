from rest_framework import serializers
from .models import Foods, Order
from account.models import User

class FoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = '__all__'
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    food = serializers.PrimaryKeyRelatedField(queryset=Foods.objects.all())
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'created_at')