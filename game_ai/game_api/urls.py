"""Game_ai URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

"""
from django.conf.urls import url
from game_api.views import bot_play, bot_play_2, bot_play_1


urlpatterns = [
    url(r'^bot/$', bot_play, name='bot'),
    url(r'^bot/neural/$', bot_play_2, name='bot2'),
    url(r'^bot/dumb/$', bot_play_1, name='bot1'),
]
