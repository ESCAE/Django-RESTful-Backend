from django.shortcuts import render
from django.http import JsonResponse
from bot import tic_tack
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.


@csrf_exempt
def bot_play(request):
    """Api end pont for bot play."""
    data = json.loads(request.body)
    import pdb; pdb.set_trace()
    request.response.headerlist.extend(
        (
            ('Access-Control-Allow-Origin',
             '*'),
            ('Content-Type', 'application/json')
        )
    )
    return JsonResponse(tic_tack.directory(data['board'], data['move']))
