from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.http import Http404

from .models import Pizza, Order
from .serializers import PizzaSerializer, OrderSerializer, OrderListSerializer, OrderDetailsSerializer
from django.db.models import Q


class PizzaList(APIView):
    """
    List of all Pizza.
    """

    def get(self, request):
        params = request.query_params
        token = params['token'] if 'token' in params.keys() else None
        available = params['available'] if 'available' in params.keys() else None
        price_range = params['price_range'].split(',') if 'price_range' in params.keys() else None
        query = Q()
        if token:
            query |= Q(name__icontains=token)
            query |= Q(brand__icontains=token)
            query |= Q(tags__name__icontains=token)
        if available:
            query &= Q(availability=available)
        if price_range and len(price_range) == 2:
            price_range_max = int(price_range[0])
            price_range_min = int(price_range[1])
            query &= Q(price__lte=price_range_max) & Q(price__gte=price_range_min)

        pizzas = Pizza.objects.filter(query).distinct()
        serializer = PizzaSerializer(pizzas, many=True)
        data = serializer.data
        for pizza in data:
            pizza['availability'] = True if pizza['availability'] == "yes" else False
        return Response(data)


class PizzaDetail(APIView):
    """
    Retrieve pizza instance.
    """

    def get_object(self, pk):
        try:
            return Pizza.objects.get(pk=pk)
        except Pizza.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pizza = self.get_object(pk)
        serializer = PizzaSerializer(pizza)
        data = serializer.data
        data['availability'] = True if data['availability'] == "yes" else False
        return Response(data)


class OrderList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    """
    List of all Order, or create a new order for a Customer.
    """

    def get(self, request):
        customer = request.user
        params = request.query_params
        order_state = params['order_state'] if 'order_state' in params.keys() else None
        date = params['date'] if 'date' in params.keys() else None
        user_id = int(params['user']) if 'user' in params.keys() else None
        if user_id:
            if user_id != customer.id:
                response = {
                    'msg': "Unauthorized !!! Provided Token User and Filter User are not same"
                }
                return Response(response, status.HTTP_401_UNAUTHORIZED)
        query = Q()
        if order_state:
            query &= Q(order_state=order_state)
        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            query &= Q(delivery_time__date=date)
        query &= Q(customer=customer)
        orders = Order.objects.filter(query).distinct()
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        response = {}
        location = request.data.get('location', "")
        request.data['latitude'] = location['lat']
        request.data['longitude'] = location['lng']
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['msg'] = "OK"
            return Response(response, status=status.HTTP_200_OK)
        response['err'] = str(serializer.errors)
        return Response(response, status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    """
    Retrieve Order instance for a Customer.
    """

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderDetailsSerializer(order)
        data = serializer.data
        data['pizza_details'] = data['pizza']
        data['customer_details'] = data['customer']
        data['location'] = {
            "lat": data['latitude'],
            "lng": data['longitude']
        }
        del data['latitude']
        del data['longitude']
        del data['pizza']
        del data['customer']
        return Response(data)
