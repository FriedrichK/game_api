from rest_framework import routers

app_name = "api"

from games.views import GameViewSet, GameUserViewSet, GameTopicViewSet

router = routers.SimpleRouter()
router.register(r"games", GameViewSet)
router.register(r"game_users", GameUserViewSet)
router.register(r"game_topics", GameTopicViewSet)
urlpatterns = router.urls
