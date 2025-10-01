from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Pereval
from .serializers import PerevalSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    operation_description="Добавление новых данных о перевале",
    request_body=PerevalSerializer,
    responses={
        200: openapi.Response('Успешное добавление', examples={
            'application/json': {
                "status": 200,
                "message": "Отправлено успешно",
                "id": 1
            }
        }),
        400: openapi.Response('Ошибка валидации', examples={
            'application/json': {
                "status": 400,
                "message": "Не указано название перевала"
            }
        })
    }
)
@api_view(['POST'])
def submit_data(request):
    serializer = PerevalSerializer(data=request.data)

    if serializer.is_valid():
        if not serializer.validated_data.get('title'):
            return Response({
                'status': 400,
                'message': 'Не указано название перевала'
            }, status=status.HTTP_400_BAD_REQUEST)

        user_data = serializer.validated_data.get('user', {})
        if not user_data.get('email') or not user_data.get('phone'):
            return Response({
                'status': 400,
                'message': 'Не указаны контактные данные пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)

        images = serializer.validated_data.get('images', [])
        if len(images) == 0:
            return Response({
                'status': 400,
                'message': 'Не добавлены фотографии перевала'
            }, status=status.HTTP_400_BAD_REQUEST)

        pereval = serializer.save()

        return Response({
            'status': 200,
            'message': 'Отправлено успешно',
            'id': pereval.id
        }, status=status.HTTP_200_OK)

    else:
        return Response({
            'status': 400,
            'message': 'Неверный формат данных',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def pereval_detail(request, pk):
    """
    Обрабатывает GET и PATCH для /submitData/<id>/
    """
    pereval = get_object_or_404(Pereval, pk=pk)

    if request.method == 'GET':
        """GET /submitData/<id>/ - получить одну запись по id"""
        serializer = PerevalSerializer(pereval)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        """PATCH /submitData/<id>/ - отредактировать запись"""
        if pereval.status != 'new':
            return Response({
                'state': 0,
                'message': 'Редактирование запрещено. Запись уже прошла модерацию.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if 'user' in request.data:
            user_data = request.data['user']
            current_user = pereval.user

            protected_fields = ['email', 'phone', 'fam', 'name', 'otc']
            for field in protected_fields:
                if field in user_data and user_data[field] != getattr(current_user, field):
                    return Response({
                        'state': 0,
                        'message': f'Запрещено изменять поле пользователя: {field}'
                    }, status=status.HTTP_400_BAD_REQUEST)

        serializer = PerevalSerializer(pereval, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'state': 1,
                'message': 'Запись успешно обновлена'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'state': 0,
                'message': 'Ошибка валидации данных',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_perevals(request):
    """
    GET /submitData/?user__email=<email> - список данных по email пользователя
    """
    email = request.GET.get('user__email')

    if not email:
        return Response({
            'message': 'Не указан параметр user__email'
        }, status=status.HTTP_400_BAD_REQUEST)

    perevals = Pereval.objects.filter(user__email=email)

    if not perevals.exists():
        return Response({
            'message': f'Для пользователя с email {email} перевалов не найдено'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = PerevalSerializer(perevals, many=True)
    return Response(serializer.data)
