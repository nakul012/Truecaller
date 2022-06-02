
from pdb import set_trace
from django.shortcuts import render
from truecaller.models import Profile, User, Contact
from truecaller.serializers import (
    LoginSerializer,
    ProfileSerializer,
    UserSerializer,
    ContactSerializer,
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import mixins, generics
from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        django_logout(request)
        return Response({"Message": "successfully logout"}, status=204)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            profile = Profile.objects.create(
                user=User.objects.last(),
                phone_number=request.data["phone_number"],
                email=request.data["email"],

            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserlistView(generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        params = request.query_params
        print(params)
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(User, pk=kwargs["pk"])
        return Response(UserSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(UserSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


class ProfileListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get(self, request, *args, **kwargs):
        params = request.query_params
        print(params)
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(Profile, pk=kwargs["pk"])
        return Response(ProfileSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(ProfileSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)


class ContactListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ContactSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.all()

    def get(self, request, *args, **kwargs):
        params = request.query_params
        print(params)
        if not "pk" in kwargs:
            return self.list(request)
        post = get_object_or_404(Contact, pk=kwargs["pk"])
        return Response(ContactSerializer(post).data, status=200)

    def post(self, request):
        data = request.data
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(ContactSerializer(post).data, status=201)
        return Response(serializer.errors, status=400)


class SpamMarkedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        phone_number = request.data.get("phone_number")
        if request.data["phone_number"] is None:
            return Response(
                {
                    "Error": "Phone number required!!"
                },
                status=400
            )
        contact = Contact.objects.filter(
            phone_number=phone_number).update(spam=True)
        profile = Profile.objects.filter(
            phone_number=phone_number).update(spam=True)
        if (contact or profile):
            return Response(
                {
                    "Message": "Contact marked as spam successfully!!"
                },
                status=200
            )
        else:
            return Response(
                {
                    "Error": "Phone number not found!!"
                },
                status=400
            )

class SearchName(APIView):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        # import ipdb; set_trace()
        params = request.query_params
        name = params.get("name")
        # name=request.data.get("name")
        if params.get("name") is None:
            return Response({"error":"name is required"},status=400)
        profile_start=Profile.objects.filter(user__username__startswith=name)
        profile_contain=Profile.objects.filter(user__username__contains=name).exclude(user__username__startswith=name)
        contact_start=Contact.objects.filter(name__startswith=name)
        contact_contain=Contact.objects.filter(name__contains=name).exclude(name__startswith=name)
        response=[]
        for contact in profile_start:
            response.append(
                {
                    "name":contact.user.username,
                    "phone_number":contact.phone_number,
                    "spam":contact.spam,
                }
            )
        for contact in contact_start:
            response.append(
                {
                    "name":contact.name,
                    "phone_number":contact.phone_number,
                    "spam":contact.spam,

                }
            )
        for contact in profile_contain:
            response.append(
                {
                    "name":contact.user.username,
                    "phone_number":contact.phone_number,
                    "spam":contact.spam,

                }
            )
        for contact in contact_contain:
            response.append(
                {
                    "name":contact.name,
                    "phone_number":contact.phone_number,
                    "spam":contact.spam,

                }
            )
        return Response(
            response,status=200
        )

class SearchPhoneNumber(APIView):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        # import ipdb; set_trace()
        params = request.query_params
        phone_number=params.get("phone_number")
        if params.get("phone_number") is None:
            return Response({
                "error":"phone_number required"
            },status=400)
        profile=Profile.objects.get(phone_number=phone_number)
        if profile:
            user=User.objects.get(id=profile.user.id,is_active=True)
            return Response({
                "name":user.username,
                "phone_number":profile.phone_number,
                "spam":profile.spam,
                "email":profile.email
            })
        else:
            contact=Contact.objects.filter(phone_number=phone_number)
            serializer=ContactSerializer(contact,many=True)
            return Response({
                serializer.data
            })