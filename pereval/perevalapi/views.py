from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from .models import *
import json


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class CoordinatesViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = CoordinatesSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class RecordViewSet(viewsets.ViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def submit_data(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response({
                'status': 200,
                'message': 'Отправлено успешно',
                'id': instance.id
            }
            )


class RecordDetailViewSet(viewsets.ViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordDetailSerializer

    def get_data_id(self, request, pk):
        instance = Record.objects.get(pk=pk)
        serializer = self.serializer_class(
                instance=instance
            )
        return Response(serializer.data)

    def get_data_email(self, request, *args, **kwargs):
        email = str(request.GET.get('user__email')).strip('<>')
        print(email)

        if not email:
            return Response({'message': 'email не указан'})

        try:
            instance = Record.objects.filter(user__email=email)
        except:
            return Response({
                'state': '0',
                'message': 'У пользователя с таким email нет записей в БД'
            })
        else:
            serializer = self.serializer_class(
                    instance=instance,
                    many=True
                )
            return Response(serializer.data)


class RecordUpdateViewSet(viewsets.ViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializerUpdate

    def update_data(self, request, pk):

        try:
            instance = Record.objects.get(pk=pk)
        except:
            return Response({
                'state': '0',
                'error': 'Такой записи не существует'
            })
        else:
            if instance.status == 'new':
                serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({
                        'state': '1',
                        'message': 'Запись успешно изменена'
                    })
            else:
                return Response({
                    'state': '0',
                    'message': 'Запись принята в работу и ее нельзя изменить'
                })
