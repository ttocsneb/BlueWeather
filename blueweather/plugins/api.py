from django.http.request import HttpRequest

from blueweather.api.decorators import api


@api(name="list")
def list_plugins(request: HttpRequest):
    return {'asdf': True}
