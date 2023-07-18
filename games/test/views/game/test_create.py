from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from games.models import Game


class TestGameViewSetCreate(TestCase):
    def setUp(self) -> None:
        self.api_client: APIClient = APIClient()

    def make_request(self, data: dict):
        url: str = reverse("api:game-list")
        return self.api_client.post(url, data=data, json=True)

    def test_success(self) -> None:
        test_game_id: str = "a1043714-e6a3-4b18-8c76-9093f4f0f6ef"
        test_data: dict = {
            "id": test_game_id,
            "min_players": 2,
            "max_players": 10,
        }

        response: Response = self.make_request(test_data)

        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code, response.content
        )

        try:
            game: Game = Game.objects.get(id=test_game_id)
        except Game.DoesNotExist:
            self.fail("expected game not found in database")
        self.assertEqual(2, game.min_players)
        self.assertEqual(10, game.max_players)
