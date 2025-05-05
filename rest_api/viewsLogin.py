from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token

User = get_user_model()

@api_view(['POST'])
@permission_classes([])
def login(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    password = data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Usuario Incorrecto", status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, user.password):
        return Response("Contraseña Incorrecta", status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})
