# rest_api/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import Producto
from .serializers import ProductoSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def lista_productos(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)