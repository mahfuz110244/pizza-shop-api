from rest_framework import serializers
from .models import Pizza, Order
from user.serializers import CustomerSerializer, CustomerOrderSerializer


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['id', 'name', 'brand', 'price', 'weight', 'availability']


class PizzaOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['name', 'brand', 'image']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'pizza', 'customer', 'order_price', 'quantity', 'order_state', 'latitude', 'longitude']


class OrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    pizza_name = serializers.CharField(source='pizza.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'pizza_name', 'customer_name', 'order_price', 'quantity', 'order_state']


class OrderDetailsSerializer(serializers.ModelSerializer):
    pizza = PizzaOrderSerializer()
    customer = CustomerOrderSerializer()

    class Meta:
        model = Order
        fields = ['id', 'pizza', 'customer', 'order_price', 'quantity', 'order_state', 'latitude',
                  'longitude', 'delivery_time']


# {
# "id": <id>
# "pizza_details":
# {
# "name": "name",
# "brand" "brand",
# ""image": "url.."
# },
# "customer_details": {
# "name": "name",
# "phone" "+88017xxxxxxxx",
# },
# "order_price": <price>,
# "quantity": <quantity>,
# "address": "address",
# "location":
# {"lat": <lat>, "lng": <lng>},
# "order_state": <state>,
# "delivery_time": datetime
# }
