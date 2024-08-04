from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_app.api.serializers import RegistrationSerializer  # Assuming you have defined RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()

        return Response({'msg':'User logged out successfully'},status = status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['Response'] = 'Registration Successful'
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key # we can also use get or create
            data['token'] = token
            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #                'refresh': str(refresh),
            #                'access': str(refresh.access_token),
            #                }


            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













# from django.contrib.auth.models import User
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from user_app.api.serializers import RegistrationSerializer  # Assuming you have defined RegistrationSerializer
# from rest_framework.authtoken.models import Token
#
# @api_view(['POST',])
# def registration_view(request):
#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             account = serializer.save()
#             data['Response'] = 'Registration Successful'
#             data['username'] = account.username
#             data['email'] = account.email
#             token = Token.objects.create(user=account).key
#             data['token'] = token
#             return Response(data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#
