from uuid import uuid4
from typing import AnyStr, Dict

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import RegisterSerializer
from account.models import UserModel
from core.cache import user_registration_cache, magic_link_cache


class RegisterView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            token = str(uuid4())

            user_registration_cache[token] = serializer.validated_data
            verification_link = request.build_absolute_uri(reverse(viewname='verify-registration', args=[token]))

            mail_message = f'Clique no link para confirmar seu cadastro: {verification_link}'
            send_mail(
                'Confirme o cadastro',
                mail_message,
                settings.DEFAULT_FROM_EMAIL,
                [serializer.validated_data['email']]
            )
            print(mail_message)

            return Response({'message': 'Email de verificação foi enviado!'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyRegistrationView(APIView):
    @staticmethod
    def get(request, token) -> Response:
        token = str(token)

        user_data: Dict[AnyStr, AnyStr] = user_registration_cache.get(token)

        if user_data:
            user = UserModel.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )

            del user_registration_cache[token]

            authenticated_user = authenticate(request, email=user.email, password=user_data['password'])

            if authenticated_user is not None:
                refresh = RefreshToken.for_user(authenticated_user)
                access_token = refresh.access_token

                return Response({
                    'message': 'Cadastro confirmado e login realizado com sucesso!',
                    'access': str(access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)

            return Response(
                data={'message': 'Usuário criado, mas erro ao autenticar.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            data={'message': 'O link de confirmação expirou ou não existe.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class EmailLoginView(APIView):
    @staticmethod
    def post(request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(data={'message': 'Email e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response(data={'message': 'Usuário não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=user.email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response(
                data={
                    'message': 'Login bem-sucedido!',
                    'access': str(access_token),
                    'refresh': str(refresh),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(data={'message': 'Senha incorreta.'}, status=status.HTTP_400_BAD_REQUEST)


class SendMagicLinkView(APIView):
    @staticmethod
    def post(request):
        email = request.data.get('email')

        if not email:
            return Response({'message': 'Email é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response({'message': 'Usuário não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

        token = str(uuid4())
        magic_link_cache[token] = user.pk

        magic_link = request.build_absolute_uri(reverse('magic-login', args=[token]))

        print(f"Magic link: {magic_link}")  # opcional

        send_mail(
            subject='Seu link mágico de login',
            message=f'Clique aqui para logar: {magic_link}',
            from_email='noreply@codeacademy.com',
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({'message': 'Link de login enviado para o seu email.'})


class MagicLinkLoginView(APIView):
    @staticmethod
    def get(request, token):
        user_pk = magic_link_cache.pop(str(token), None)

        if not user_pk:
            return Response(data={'message': 'Link inválido ou expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(pk=user_pk)
        except UserModel.DoesNotExist:
            return Response(data={'message': 'Usuário não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response(
            data={
                'message': 'Login via link mágico bem-sucedido!',
                'access': str(access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_200_OK
        )