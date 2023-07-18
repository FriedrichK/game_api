from django.urls import path

from conductor.views import CreateGameAPIView, JoinGameAPIView

app_name = "conductor"

urlpatterns = [
    path('create_game/', CreateGameAPIView.as_view(), name='create_game'),
    path('join_game/', JoinGameAPIView.as_view(), name='join_game')
]
