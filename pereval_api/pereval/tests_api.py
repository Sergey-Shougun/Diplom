from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PerevalAPITests(APITestCase):

    def setUp(self):
        self.test_data = {
            "beauty_title": "пер.",
            "title": "Тестовый перевал",
            "other_titles": "Тест",
            "connect": "",
            "add_time": "2021-09-22 13:18:13",
            "user": {
                "email": "test@example.com",
                "phone": "+79001234567",
                "fam": "Иванов",
                "name": "Иван",
                "otc": "Иванович"
            },
            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200"
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
                    "title": "Тестовое изображение"
                }
            ]
        }

    def test_complete_workflow(self):

        print("1. Тестируем создание перевала...")
        url = reverse('submit_data')
        response = self.client.post(url, self.test_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 200)
        pereval_id = response.data['id']
        print(f"✅ Создан перевал с ID: {pereval_id}")

        print("2. Тестируем получение перевала по ID...")
        url = reverse('pereval_detail', kwargs={'pk': pereval_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Тестовый перевал")
        self.assertEqual(response.data['status'], 'new')
        print("✅ Данные перевала получены корректно")

        print("3. Тестируем обновление перевала...")
        update_data = {
            "title": "Обновленное название",
            "level": {
                "summer": "2А"
            }
        }
        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 1)
        print("✅ Перевал успешно обновлен")

        print("4. Проверяем обновленные данные...")
        response = self.client.get(url)
        self.assertEqual(response.data['title'], "Обновленное название")
        self.assertEqual(response.data['level']['summer'], "2А")
        print("✅ Данные корректно обновились")

        print("5. Тестируем фильтрацию по email...")
        url = reverse('get_user_perevals') + '?user__email=test@example.com'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['email'], 'test@example.com')
        print("✅ Фильтрация по email работает корректно")

        print("🎉 Все тесты пройдены успешно!")

    def test_validation_errors(self):

        invalid_data = self.test_data.copy()
        invalid_data['title'] = ''

        url = reverse('submit_data')
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_data_protection(self):

        url = reverse('submit_data')
        response = self.client.post(url, self.test_data, format='json')
        pereval_id = response.data['id']

        update_data = {
            "user": {
                "email": "hacker@example.com"
            }
        }

        url = reverse('pereval_detail', kwargs={'pk': pereval_id})
        response = self.client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['state'], 0)