from curses.ascii import US
from datetime import datetime

from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
# from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from django.views.decorators.csrf import csrf_exempt
from .models import User

from .serializers import ( RegistrationSerializer , LoginSerializer , UserSerializer,DashboardSerializer)


from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return redirect('login')

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):

    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')

@method_decorator(login_required, name='dispatch')
class profile(TemplateView):
    template_name = 'authentication/profile.html'
    def get(self,request,*args, **kwargs):
        self.username = request.user.username
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['json_data'] = User.objects.get(username = self.username)
        return context

# registration method for registring new user
class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# login method when user need to login.
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

        
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        # print("test")
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        person = request.user
        self.check_object_permissions(request, person)
        serializer = DashboardSerializer(person)
        return Response(serializer.data)
