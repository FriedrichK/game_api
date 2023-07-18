from typing import Optional

from rest_framework import serializers

from games.models import Game, GameUser, GameTopic


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ("id", "name", "min_players", "max_players", "created", "started")


class GameUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        game: Optional[str] = self.context.get("game")
        if game is None:
            raise serializers.ValidationError({"game": ["invalid or missing"]})
        validated_data["game"] = game
        return super().create(validated_data)

    class Meta:
        model = GameUser
        fields = ("id", "game", "name", "created")


class GameTopicSerializer(serializers.ModelSerializer):
    label = serializers.CharField(required=False)

    def create(self, validated_data):
        game: Optional[str] = self.context.get("game")
        if game is None:
            raise serializers.ValidationError({"game": ["invalid or missing"]})
        validated_data["game"] = game

        player: Optional[str] = self.context.get("player")
        if player is None:
            raise serializers.ValidationError({"player": ["invalid or missing"]})

        validated_data["game"] = game

        validated_data["label"] = "whatever"

        return super().create(validated_data)

    class Meta:
        model = GameTopic
        fields = ("id", "game", "player", "label", "created")
