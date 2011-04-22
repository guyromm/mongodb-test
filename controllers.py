from noodles.http import Response

def index(request):
    return Response("<h1>Hello Mongo DB test!</h1>")