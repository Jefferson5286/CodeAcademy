from rest_framework.serializers import CharField, EmailField, ModelSerializer

from account.models import UserModel


class RegisterSerializer(ModelSerializer):
    username = CharField(max_length=150)
    password = CharField(write_only=True)
    email = EmailField()

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password')
