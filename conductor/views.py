import requests
from django.conf import settings
from requests import Response
from rest_framework import serializers, status
from rest_framework.response import Response as APIResponse
from rest_framework.views import APIView


class CreateGameViewSerializer(serializers.Serializer):
    name = serializers.CharField()
    min_players = serializers.IntegerField()
    max_players = serializers.IntegerField()


class CreateGameAPIView(APIView):
    def post(self, request):
        serializer = CreateGameViewSerializer(data=request.data)
        serializer.is_valid()

        endpoint: str = settings.CONDUCTOR_API_ENDPOINT + "/workflow/play_game_round"

        data: dict = {
            "name": serializer.validated_data.get("name"),
            "min_players": serializer.validated_data.get("min_players"),
            "max_players": serializer.validated_data.get("max_players"),
        }

        response: Response = requests.post(endpoint, json=data)
        if response.status_code != status.HTTP_200_OK:
            return APIResponse(status=response.status_code, data=response.content)
        return APIResponse(data={"game_id": response.content})


class JoinGameViewSerializer(serializers.Serializer):
    game_id = serializers.CharField()
    name = serializers.CharField()
    password = serializers.CharField()


class JoinGameAPIView(APIView):
    def post(self, request):
        serializer = JoinGameViewSerializer(data=request.data)
        serializer.is_valid()

        endpoint: str = settings.CONDUCTOR_API_ENDPOINT + "/workflow/add_player"

        data: dict = {
            "game_round_workflow_id": serializer.validated_data.get("game_id"),
            "player_name": serializer.validated_data.get("name"),
            "player_password": serializer.validated_data.get("password"),
        }
        print(data)

        response: Response = requests.post(endpoint, json=data)
        if response.status_code != status.HTTP_200_OK:
            return APIResponse(status=response.status_code, data=response.content)
        return APIResponse(data={"player_id": response.content})
