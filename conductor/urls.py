from django.urls import path

from conductor.views import CreateGameAPIView

app_name = "conductor"

urlpatterns = [
    path('create_game/', CreateGameAPIView.as_view(), name='create_game')
]
