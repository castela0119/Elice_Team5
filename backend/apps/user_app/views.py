# Create your views here.

from .serializers import RegistrationSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = RegistrationSerializer(data=request.data)
        
            data = {}
        
            if serializer.is_valid():
                account = serializer.save()
                
                data['response'] = "Registration Successful!"
                data['username'] = account.username
                data['email'] = account.email

                # token = Token.objects.get(user=account).key
                # data['token'] = token

                # refresh = RefreshToken.for_user(account)
                # data['token'] = {
                #                     'refresh': str(refresh),
                #                     'access': str(refresh.access_token),
                #                 }
        
            else:
                data = serializer.errors
        
            return Response(data, status=status.HTTP_201_CREATED)