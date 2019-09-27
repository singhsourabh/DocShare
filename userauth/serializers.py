from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        pw = data.get('password')
        pw1 = data.pop('password1')
        if pw != pw1:
            raise serializers.ValidationError(
                "Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj
