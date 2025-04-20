from rest_framework.serializers import *

from account.models import UserModel


class RegisterSerializer(ModelSerializer):
    username = CharField(max_length=150)
    password = CharField(write_only=True)
    email = EmailField()

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password')


class TutorPermissionSerializer(Serializer):
    user_id = UUIDField()

    @staticmethod
    def validate_user_id(value):
        """
            Valida se o usuário existe.
        """
        try:
            user = UserModel.objects.get(id=value)
        except UserModel.DoesNotExist:
            raise ValidationError("Usuário não encontrado.")
        return value

    def create(self, validated_data):
        """
            Concede permissão de tutor ao usuário.
        """
        user = UserModel.objects.get(id=validated_data['user_id'])
        user.is_tutor = True
        user.save()
        return user