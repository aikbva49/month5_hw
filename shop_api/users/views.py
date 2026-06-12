import random
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import RegisterValidateSerializer, AuthValidateSerializer, UserConfirmSerializer
from .models import UserSMSCode

@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )
    
    generated_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    
    UserSMSCode.objects.create(user=user, code=generated_code)
    
    return Response(
        status=status.HTTP_201_CREATED,
        data={'user_id': user.id, 'code': generated_code}
    )

@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = authenticate(**serializer.validated_data)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Неверные данные или аккаунт не активирован'})

@api_view(['POST'])
def confirm_api_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    username = serializer.validated_data['username']
    received_code = serializer.validated_data['code']
    
    try:
        user = User.objects.get(username=username)
        user_code_obj = UserSMSCode.objects.get(user=user)
    except (User.DoesNotExist, UserSMSCode.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Код или пользователь не найден'})
    
    if user_code_obj.code == received_code:
        user.is_active = True  
        user.save()
        user_code_obj.delete()  
        return Response(status=status.HTTP_200_OK, data={'message': 'Успешно подтверждено!'})
    
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Неверный код'})
