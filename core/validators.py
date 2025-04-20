from re import sub
from django.core.exceptions import ValidationError


def validar_cpf(value):
    cpf = sub(r'[^0-9]', '', value)

    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos.')

    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido: todos os dígitos iguais.')

    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10

        if int(cpf[i]) != digito:
            raise ValidationError('CPF inválido.')
