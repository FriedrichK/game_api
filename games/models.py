from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Game(BaseModel):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=32)
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    started = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True)


class GameUser(BaseModel):
    id = models.CharField(max_length=36, primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)


class GameTopic(BaseModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(GameUser, on_delete=models.CASCADE)
    label = models.CharField(max_length=128)
