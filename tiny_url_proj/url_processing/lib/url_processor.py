import json

from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, FieldError, FieldDoesNotExist, RequestAborted

from ..models import Url
from .helper import format_datetime, is_correct, generate_tiny_url


class UrlProcessor:
    MAX_ATTEMPTS = 1000  # number of attempts during random tiny_url generation

    @staticmethod
    @transaction.atomic
    def get_original_url_and_update(tiny_url):
        """Method is fetching data and updating statistics when
            tiny_url is presenting in the DB as atomic transaction
        Args:
            tiny_url: shorten url to find
        Returns:
            Original_url
        """
        try:
            u = Url.objects.get(pk=tiny_url)
            u.counter += 1
            u.last_request_date = timezone.now()
            u.save()
            return u.original_url
        except Exception as e:
            raise ObjectDoesNotExist

    @staticmethod
    def get_stats(tiny_url):
        """Receiving statistics by tiny_url
        Args:
            tiny_url: shorten url to find
        Returns:
            statistics
        """
        try:
            u = Url.objects.get(pk=tiny_url)
            url_stats = {
                "created": format_datetime(u.created_date),
                "lastRedirect": format_datetime(u.last_request_date),
                "redirectCount": u.counter
            }
            stats = json.dumps(url_stats)
            return stats
        except Exception as e:
            raise ObjectDoesNotExist

    @staticmethod
    @transaction.atomic
    def add_original_url(request):
        """Given an url, return tiny_url, create if necessary.
        Args:
            original_url: url to shorten.
        Returns:
            Returns tiny_url
        """
        try:
            req = json.loads(request.body.decode('utf-8'))
            orig_url = req['url']
            tiny_url = req.get('shortcode', None)

            if not tiny_url:
                counter = 0
                while counter < UrlProcessor.MAX_ATTEMPTS:
                    tiny_url = generate_tiny_url()
                    try:
                        Url.objects.get(pk=tiny_url)
                        counter += 1
                    except ObjectDoesNotExist:
                        u = Url(
                                tiny_url=tiny_url,
                                original_url=orig_url,
                                counter=0,
                                created_date=timezone.now(),
                                last_request_date=timezone.now()
                            )
                        u.save()
                        return json.dumps({'shortcode': tiny_url})
                if counter >= UrlProcessor.MAX_ATTEMPTS:
                    raise FieldError

            if is_correct(tiny_url):
                try:
                    Url.objects.get(pk=tiny_url)
                    raise RequestAborted  # there is already such tiny_url
                except ObjectDoesNotExist:
                    u = Url(
                            tiny_url=tiny_url,
                            original_url=orig_url,
                            counter=0,
                            created_date=timezone.now(),
                            last_request_date=timezone.now()
                        )
                    u.save()
                    return json.dumps({'shortcode': tiny_url})
            else:
                raise FieldError
        except KeyError:
            raise FieldDoesNotExist
