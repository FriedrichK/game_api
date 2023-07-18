from typing import Optional

from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from games.models import Game, GameUser, GameTopic
from games.serializers import GameSerializer, GameUserSerializer, GameTopicSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by("-created")
    pagination_class = CustomPageNumberPagination
    serializer_class = GameSerializer


class GameUserViewSet(viewsets.ModelViewSet):
    queryset = GameUser.objects.all().order_by("created")
    serializer_class = GameUserSerializer

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = super().get_queryset()
        game_id: Optional[str] = self.request.GET.get("game")
        if game_id:
            queryset = queryset.filter(game__id=game_id)
        return queryset

    def get_serializer_context(self) -> dict:
        serializer_context: dict = super().get_serializer_context()
        game_id: str = self.request.data.get("game")
        if game_id:
            try:
                serializer_context["game"] = Game.objects.get(id=game_id)
            except Game.DoesNotExist:
                pass
        return serializer_context


class GameTopicViewSet(viewsets.ModelViewSet):
    queryset = GameTopic.objects.all()
    serializer_class = GameTopicSerializer

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = super().get_queryset()
        game_id: Optional[str] = self.request.GET.get("game")
        if game_id:
            queryset = queryset.filter(game__id=game_id)
        return queryset

    def get_serializer_context(self) -> dict:
        serializer_context: dict = super().get_serializer_context()
        game_id: str = self.request.data.get("game")
        if game_id:
            try:
                serializer_context["game"] = Game.objects.get(id=game_id)
            except Game.DoesNotExist:
                pass
        player_id: str = self.request.data.get("player")
        if player_id:
            try:
                serializer_context["player"] = GameUser.objects.get(id=player_id)
            except GameUser.DoesNotExist:
                pass
        return serializer_context
