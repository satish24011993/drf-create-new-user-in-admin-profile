from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView, View
from rest_framework import viewsets
# Create your views here.
from api.models import User,UserProfile
from api.serializers import UserSerializer,UserProfileSerializer, LoginSerializer
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser, IsUpdateProfile, UserIsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from rest_framework.renderers import TemplateHTMLRenderer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        renderer_classes = [TemplateHTMLRenderer]
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            # permission_classes = [IsLoggedInUserOrAdmin,IsAdminUser,IsAuthenticated]
            permission_classes = [IsAuthenticated, UserIsOwnerOrReadOnly]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ProfileAPI(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.kwargs['user_id'])

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, UserIsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


# class ProfileViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated, UserIsOwnerOrReadOnly]

#     def partial_update(self, request, pk=None): #partially update the profile
#         try:
#             user_detail = User.objects.get(pk=pk)
#             print(user_detail)
#             serializer = UserSerializer(user_detail,data=request.data, partial = True)
#         # serializer = UserProfileSerializer(user_detail, data=request.data)
#             if not serializer.is_valid():
#                 return Response({'data':'internal server error', 'message': 'got error!'}, 500)
#         # if serializer.is_valid():
#             serializer.save()   
        
#         except Exception as e:
#             return Response('some exception occured' + str(e))
        
#         # return Response('Unknown')
#         return Response('record Updated successfully')
    
#     def retrieve(self, request, pk=None):

#         queryset = User.objects.get(pk=pk)

#         serializer_class = UserSerializer(queryset)

#         return Response(serializer_class.data)



# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'profile_list.html'

#     # Add this code block
#     def get_permissions(self, request):
#         permission_classes = []
#         if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsAuthenticated, UserIsOwnerOrReadOnly]
#         elif self.action == 'list' or self.action == 'destroy':
#             permission_classes = [IsAdminUser]
#         # return [permission() for permission in permission_classes]
#         for permission in permission_classes:
#             return permission()
        

class ProfileViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_list.html'
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        queryset = User.objects.all()
        return Response({'profiles': queryset})

        
    
    # def get_permissions(self, request):
    #     permission_classes = []
    #     if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsAuthenticated, UserIsOwnerOrReadOnly]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     # return [permission() for permission in permission_classes]
    #     for permission in permission_classes:
    #         return Response(permission())

# class LoginView(View):
#     serializer_class = LoginSerializer
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'login.html'
#     permission_classes = (IsAuthenticated)

#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(request.POST)
#         if form.is_valid():

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            post_data = {'username':  form.cleaned_data['username'],'password': form.cleaned_data['password']}
            response = requests.post('http://127.0.0.1:8000/api/api-auth/login/', data=post_data)
            return HttpResponseRedirect('/profile/')


class ProfileDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_detail.html'

    def get(self, request, pk):
        profile = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return redirect('profile-list')

class ProductListAPIView(ProductListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    filter_fields = (
        'category__id',
    )
    search_fields = (
        'title',
    )