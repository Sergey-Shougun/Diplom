from .models import Coords, Level
from .serializers import PerevalSerializer, UserSerializer, CoordsSerializer, LevelSerializer, ImageSerializer
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Pereval, User
import os
import django
from django.test import TestCase


class WSGIASGITests(TestCase):

    def test_wsgi_application(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pereval_api.settings')
        django.setup()

        from pereval_api.wsgi import application
        self.assertIsNotNone(application)
        print("✅ WSGI приложение инициализируется")

    def test_asgi_application(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pereval_api.settings')
        django.setup()

        from pereval_api.asgi import application
        self.assertIsNotNone(application)
        print("✅ ASGI приложение инициализируется")


class ViewsEdgeCaseTests(APITestCase):

    def setUp(self):
        self.base_data = {
            "beauty_title": "пер.",
            "title": "Крайний случай",
            "other_titles": "Тест",
            "connect": "",
            "add_time": "2021-09-22 13:18:13",
            "user": {
                "email": "edge_case@example.com",
                "phone": "+79005556677",
                "fam": "Крайний",
                "name": "Случай",
                "otc": "Тестович"
            },
            "coords": {
                "latitude": "48.1234",
                "longitude": "10.5678",
                "height": "2000"
            },
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""
            },
            "images": [
                {
                    "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
                    "title": "Крайнее фото"
                }
            ]
        }

    def test_submit_data_missing_required_fields(self):
        invalid_data = self.base_data.copy()
        invalid_data.pop('title')

        url = reverse('submit_data')
        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 400)
        print("✅ Обработка отсутствующего title работает")

        invalid_data = self.base_data.copy()
        invalid_data['user'].pop('email')

        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("✅ Обработка отсутствующего email работает")

    def test_submit_data_empty_images(self):
        invalid_data = self.base_data.copy()
        invalid_data['images'] = []

        url = reverse('submit_data')
        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 400)
        print("✅ Обработка пустого массива изображений работает")

    def test_update_non_existent_pereval(self):
        url = reverse('pereval_detail', kwargs={'pk': 99999})
        update_data = {"title": "Несуществующий"}

        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("✅ Обработка несуществующего перевала работает")

    def test_get_non_existent_pereval(self):
        url = reverse('pereval_detail', kwargs={'pk': 99999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("✅ Получение несуществующего перевала обрабатывается")

    def test_get_user_perevals_empty_result(self):
        url = reverse('get_user_perevals') + '?user__email=nonexistent@example.com'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("✅ Обработка отсутствующих перевалов пользователя работает")

    def test_update_pereval_not_new_status(self):
        url = reverse('submit_data')
        response = self.client.post(url, self.base_data, format='json')
        pereval_id = response.data['id']

        pereval = Pereval.objects.get(id=pereval_id)
        pereval.status = 'accepted'
        pereval.save()

        url = reverse('pereval_detail', kwargs={'pk': pereval_id})
        update_data = {"title": "Попытка обновления"}
        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['state'], 0)
        print("✅ Запрет обновления перевала не в статусе 'new' работает")


class SerializerTests(TestCase):

    def setUp(self):
        self.user_data = {
            "email": "serializer_test@example.com",
            "phone": "+79002223344",
            "fam": "Сидоров",
            "name": "Сидор",
            "otc": "Сидорович"
        }

        self.coords_data = {
            "latitude": "47.8912",
            "longitude": "9.3456",
            "height": "1800"
        }

        self.level_data = {
            "winter": "2А",
            "summer": "1Б",
            "autumn": "1Б",
            "spring": "1А"
        }

        self.image_data = {
            "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
            "title": "Сериализатор тест"
        }

    def test_user_serializer_validation(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

        invalid_data = self.user_data.copy()
        invalid_data['email'] = "invalid-email"
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        print("✅ Валидация UserSerializer работает")

    def test_coords_serializer_validation(self):
        serializer = CoordsSerializer(data=self.coords_data)
        self.assertTrue(serializer.is_valid())
        print("✅ Валидация CoordsSerializer работает")

    def test_level_serializer_validation(self):
        serializer = LevelSerializer(data=self.level_data)
        self.assertTrue(serializer.is_valid())
        print("✅ Валидация LevelSerializer работает")

    def test_image_serializer_validation(self):
        serializer = ImageSerializer(data=self.image_data)
        self.assertTrue(serializer.is_valid())
        print("✅ Валидация ImageSerializer работает")

    def test_pereval_serializer_partial_update(self):
        user = User.objects.create(**self.user_data)
        coords = Coords.objects.create(**self.coords_data)
        level = Level.objects.create(**self.level_data)

        pereval = Pereval.objects.create(
            beauty_title="пер. тест",
            title="Тестовый перевал",
            other_titles="Тест",
            connect="",
            add_time=timezone.now(),
            user=user,
            coords=coords,
            level=level,
            status="new"
        )

        update_data = {
            "title": "Обновленное название",
            "level": {
                "summer": "2А"
            }
        }

        serializer = PerevalSerializer(instance=pereval, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_pereval = serializer.save()

        self.assertEqual(updated_pereval.title, "Обновленное название")
        self.assertEqual(updated_pereval.level.summer, "2А")
        print("✅ Частичное обновление PerevalSerializer работает")
