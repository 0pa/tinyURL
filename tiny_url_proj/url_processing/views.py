from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, FieldError, FieldDoesNotExist, RequestAborted
from django.views.decorators.csrf import csrf_exempt

from .lib.url_processor import UrlProcessor


def index(request):
    return HttpResponse("Hello, it's tinyURL test task!")


def get_stats(request, tiny_url):
    if request.method == 'GET':
        try:
            stats = UrlProcessor.get_stats(tiny_url)
            return HttpResponse(stats, status=200)
        except ObjectDoesNotExist:
            return HttpResponse('Shortcode not found', status=404)


def get_original_url(request, tiny_url):
    """Fetch original url by tiny_url
    Args:
        request: request object
        tiny_url: tiny url code
    """
    if request.method == 'GET':
        try:
            original_url = UrlProcessor.get_original_url_and_update(tiny_url)
            return HttpResponse(status=302,
                                headers={'Location': f'{original_url}'}
                                )
        except ObjectDoesNotExist:
            return HttpResponse('Shortcode not found', status=404)


@csrf_exempt
def add_new_url(request):
    """Adding new url,
    Args:
        request: {
                    "url": "https://www.example.com/",
                    "shortcode": "abn123"
                }

    """
    if request.method == 'POST':
        try:
            resp = UrlProcessor.add_original_url(request)
            return HttpResponse(resp, status=201)
        except FieldDoesNotExist:
            return HttpResponse('Url not present', status=400)
        except FieldError:
            return HttpResponse('The provided shortcode is invalid', status=412)
        except RequestAborted:
            return HttpResponse('Shortcode already in use', status=409)
