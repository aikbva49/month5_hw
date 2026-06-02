from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Film
from .serializers import FilmSerializer


api_view(['GET'])
def film_list_api_view(request):
    dict_ = {
        'text' : 'Hello world',
        'active' : True,
        'integer' : 100,
        'float' : 12.5,
        'list' : [1, 2, 3, 4, 5],
    }
    return Response(dict_)













