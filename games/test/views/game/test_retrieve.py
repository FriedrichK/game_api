from datetime import datetime

import arrow
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from games.models import Game


@freeze_time("2022-03-04 05:06:07")
class TestGameViewSetUpdate(TestCase):
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

    def make_request(self):
        url: str = reverse("api:game-detail", kwargs={"pk": self.test_game_id})
        return self.api_client.get(url, json=True)

    def test_success(self) -> None:
        response: Response = self.make_request()

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)

        expected: dict = {
            "created": "2022-03-04T05:06:07Z",
            "id": "a1043714-e6a3-4b18-8c76-9093f4f0f6ef",
            "max_players": 10,
            "min_players": 2,
            "started": None,
        }
        self.assertDictEqual(expected, response.json())
