from datetime import datetime

import arrow
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from games.models import Game


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

    def make_request(self, data: dict):
        url: str = reverse("api:game-detail", kwargs={"pk": self.test_game_id})
        return self.api_client.patch(url, data=data, json=True)

    def test_success(self) -> None:
        start_time: datetime.datetime = arrow.get(2023, 6, 1, 15, 24, 3).datetime
        test_data: dict = {"started": arrow.get(start_time).format()}

        response: Response = self.make_request(test_data)

        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)

        self.test_game.refresh_from_db()

        self.assertEqual(start_time, self.test_game.started)
