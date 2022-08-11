from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

class ProductAPIS(APIView):
    
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    
    def get(self,request, pk=None, format=None):
        
        if pk is not None:
            try:
                product = Product.objects.get(_id=pk)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except Exception as e:
                return Response({"message": str(e)})
        
        
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data})      
      
    def post(self, request,format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Product Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Product details Updated'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
                return Response({"message": "Product Not Found"})
    
    def delete(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'msg':'Product Deleted'})
        except Product.DoesNotExist:
                return Response({"message": "Product Not Found"})
    