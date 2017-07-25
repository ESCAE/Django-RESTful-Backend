"""Api end points."""
from bot import tic_tack
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def bot_play(request):
    """End point for bot play."""
    data = json.loads(request.body)
    return JsonResponse(tic_tack.directory(data['board'], data['move']))


def home(request):
    """End pont for root.

    For testing purposes. May contain info at some point.
    """
    return HttpResponse("<h1>Hello World!</h1>")
