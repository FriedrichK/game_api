import uuid
from typing import List

from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from games.models import Game, GameUser
from games.serializers import GameUserSerializer


@freeze_time("2022-03-04 05:06:07")
class TestGameUserViewSetCreate(TestCase):
    maxDiff = None

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

        self.game_users: List[GameUser] = []
        for i in range(10):
            game_user: GameUser = GameUser(
                id=str(uuid.uuid4()), game=self.test_game, name=f"Test User {i + 1}"
            )
            game_user.save()
            self.game_users.append(game_user)

        self.test_game2: Game = Game(
            id="58703a37-3829-475e-ad23-01f7d4fcdd3a",
            min_players=2,
            max_players=10,
            started=None,
        )

        # another game is running in parallel, with its own users
        self.test_game2.save()
        for i in range(10):
            game_user: GameUser = GameUser(
                id=str(uuid.uuid4()), game=self.test_game2, name=f"Test User {i + 1}"
            )
            game_user.save()

    def make_request(self, game_id: str) -> Response:
        url: str = reverse("api:gameuser-list")
        params: dict = {"game": game_id} if game_id else {}
        return self.api_client.get(url, data=params, json=True)

    def test_success(self) -> None:
        response: Response = self.make_request(self.test_game_id)

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)

        expected: dict = {
            "count": 10,
            "next": None,
            "previous": None,
            "results": [
                GameUserSerializer(game_user).data for game_user in self.game_users
            ],
        }
        self.assertDictEqual(expected, response.json())
