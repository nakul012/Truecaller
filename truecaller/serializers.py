from django.contrib.auth import get_user_model
from truecaller.models import Profile, Contact
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


# User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data["username"]
        password = data["password"]

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    raise ValidationError("User is deactivated")
            else:
                raise ValidationError("Unable to login with given credentials")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    # def validate(self, attrs):
    #     # import ipdb; ipdb.set_trace()
    #     # return super().validate(attrs)

    def create(self, validated_data):
        # super().create(validated_data)

        # print(validated_data)
        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            password=make_password(validated_data["password"])
            # phone=validated_data["phone"],
        )

        # why we use def create here
        return user
    # def create(self, validated_data):
    #     return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:

        model = Profile
        fields = '__all__'

    # def create(self, validated_data):
    #     # super().create(validated_data)

    #     # print(validated_data)
    #     profile = Profile.objects.create(
    #                 email=validated_data.data["email"],
	#         		user=User.objects.get(email=email),
    #                 phone_number=validated_data.data["phone_number"],
    #                 spam=True)
    #         # phone=validated_data ["phone"],

        # why we use def create here
        # return profile


class ContactSerializer(serializers.ModelSerializer):
    class Meta:

        model = Contact
        fields = '__all__'

    # def create(self, validated_data):
    #     # super().create(validated_data)

    #     # print(validated_data)
    #     contact = Contact.objects.create(
    #                 email=validated_data.data["email"],
	#         		user=User.objects.get(email=email,
    #                 phone_number=validated_data.data["phone_number"],
    #                 spam=True)
    #         # phone=validated_data["phone"],

    #     # why we use def create here
    #     return contact
