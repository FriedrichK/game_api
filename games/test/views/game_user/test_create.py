from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from games.models import Game, GameUser


class TestGameUserViewSetCreate(TestCase):
    def setUp(self) -> None:
        self.api_client: APIClient = APIClient()

        self.test_game_id: str = "a1043714-e6a3-4b18-8c76-9093f4f0f6ef"
        self.test_game: Game = Game(
            id=self.test_game_id,
            min_players=2,
            max_players=10,
            started=None,
        )
        self.test_game.save()

    def make_request(self, data: dict):
        url: str = reverse("api:gameuser-list")
        return self.api_client.post(url, data=data, json=True)

    def test_success(self) -> None:
        test_game_user_id: str = "ae65d1bc-055a-48a4-8853-3b64f1cde01c"
        test_data: dict = {
            "id": test_game_user_id,
            "game": self.test_game_id,
            "name": "Jane Doe",
        }

        response: Response = self.make_request(test_data)

        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code, response.content
        )

        try:
            game_user: GameUser = GameUser.objects.get(id=test_game_user_id)
        except Game.DoesNotExist:
            self.fail("expected game user not found in database")
        self.assertEqual("Jane Doe", game_user.name)
