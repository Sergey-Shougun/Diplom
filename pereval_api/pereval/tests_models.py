from django.test import TestCase
from .models import User, Coords, Level, Pereval
from django.utils import timezone


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            phone="+79001234567",
            fam="Иванов",
            name="Иван",
            otc="Иванович"
        )

        self.coords = Coords.objects.create(
            latitude=45.3842,
            longitude=7.1525,
            height=1200
        )

        self.level = Level.objects.create(
            winter="",
            summer="1А",
            autumn="1А",
            spring=""
        )

    def test_user_creation(self):
        """Тест создания пользователя"""
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.phone, "+79001234567")

    def test_pereval_creation(self):
        """Тест создания перевала"""
        pereval = Pereval.objects.create(
            beauty_title="пер.",
            title="Тестовый перевал",
            other_titles="Тест",
            connect="",
            add_time=timezone.now(),
            user=self.user,
            coords=self.coords,
            level=self.level,
            status="new"
        )

        self.assertEqual(pereval.title, "Тестовый перевал")
        self.assertEqual(pereval.status, "new")