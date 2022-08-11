from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from datetime import datetime

from .serializers import OrderSerializer
from .models import Order, OrderItem, ShippingAddress
from product.models import Product 

class UserOrdersAPIs(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self,request,pk=None, format=None):
        user = request.user
        
        if pk is not None:
            try:
                order = user.order_set.get(_id=pk)
                if user.is_staff or order.user == user:
                    serializer = OrderSerializer(order)
                    return Response(serializer.data)
                else:
                    Response({'detail': 'Not authorized to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        orders = user.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def put(self,request,pk=None, format=None):
        order = Order.objects.get(_id=pk)
        order.isPaid = True
        order.paidAt = datetime.now()
        order.save()

        return Response('Order was paid')

class AdminOrdersAPIs(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,IsAdminUser,)
    
    def get(self,request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def put(self,request,pk=None, format=None):
        order = Order.objects.get(_id=pk)
        order.isDelivered = True
        order.deliveredAt = datetime.now()
        order.save()
        return Response('Order was delivered')
    
class OrderItemsAPIs(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        
        user = request.user
        data = request.data
        orderItems = data['orderItems']
        # check for existing orders
        if orderItems and len(orderItems) == 0:
            return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            order = Order.objects.create(
                user=user,
                paymentMethod=data['paymentMethod'],
                taxPrice=data['taxPrice'],
                shippingPrice=data['shippingPrice'],
                totalPrice=data['totalPrice']
            )

            # Add shipping address
            ShippingAddress.objects.create(
                order=order,
                address=data['shippingAddress']['address'],
                city=data['shippingAddress']['city'],
                postalCode=data['shippingAddress']['postalCode'],
                country=data['shippingAddress']['country'],
            )

            # add order items
            # add order to orderItem relationship
            for i in orderItems:
                product = Product.objects.get(_id=i['product'])
                item = OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    qty=i['qty'],
                    price=i['price'],
                    image=product.image.url,
                )
                
                # Update stock
                product.countInStock -= int(item.qty)
                product.save()

            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)