import uuid

from django.db.models import *


class Curso(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = CharField(max_length=100)
    description = TextField()

class Aula(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = CharField(max_length=100)
    description = TextField()
    content = TextField()
    created = DateField(auto_now_add=True)
    curso = ForeignKey(to='api.Curso', on_delete=CASCADE, null=True, blank=True)
    order = PositiveIntegerField(default=0, null=True, blank=True)
