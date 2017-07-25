from django.shortcuts import render
from django.http import JsonResponse
from bot import tic_tack
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



@csrf_exempt
def bot_play(request):
    """Api end pont for bot play."""
    data = json.loads(request.body)
    return JsonResponse(tic_tack.directory(data['board'], data['move']))


def home(request):
    """Api end pont for bot play."""
    return HttpResponse("<h1>Hello World!</h1>")
