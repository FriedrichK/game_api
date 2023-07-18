from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from games.models import Game, GameUser, GameTopic


class TestGameTopicViewSetCreate(TestCase):
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

        self.test_game_user_id: str = "ae65d1bc-055a-48a4-8853-3b64f1cde01c"
        self.test_game_user: GameUser = GameUser(
            id=self.test_game_user_id,
            game=self.test_game,
            name="Jane Doe"
        )
        self.test_game_user.save()

    def make_request(self, data: dict):
        url: str = reverse("api:gametopic-list")
        return self.api_client.post(url, data=data, json=True)

    def test_success(self) -> None:
        test_data: dict = {
            "game": self.test_game_id,
            "player": self.test_game_user_id,
        }

        response: Response = self.make_request(test_data)

        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code, response.content
        )

        try:
            game_topic: GameTopic = GameTopic.objects.get()
        except GameTopic.DoesNotExist:
            self.fail("expected game topic not found in database")
        self.assertEqual(self.test_game, game_topic.game)
        self.assertEqual(self.test_game_user, game_topic.player)
