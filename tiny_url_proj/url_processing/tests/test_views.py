import json

from django.utils import timezone
from django.test import TestCase

from ..models import Url


class MyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        current_datetime = timezone.now()
        Url.objects.create(
            tiny_url='test12',
            original_url='http://google.com',
            counter=0,
            created_date=current_datetime,
            last_request_date=current_datetime
        )

    def test_get_stats(self):
        response = self.client.get('/test12/stats/')
        url_stat = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(url_stat["redirectCount"], 0)

    def test_get_nonexisting_stats(self):
        response = self.client.get('/test13/stats/')
        self.assertEqual(response.status_code, 404)

    def test_short_url_exists(self):
        response = self.client.get('/test12/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://google.com')

    def test_get_stats_after_changing_counter(self):
        self.test_short_url_exists()
        response = self.client.get('/test12/stats/')
        url_stat = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(url_stat["redirectCount"], 1)

    def test_add_new_url(self):
        response = self.client.post('/shorten/',
                                    """{
                                        "url": "https://www.example.com/",
                                        "shortcode": "abn123"
                                    }""",
                                    content_type="application/json"
                                    )
        self.assertEqual(response.status_code, 201)
        resp_content = json.loads(response.content)
        self.assertEqual(resp_content['shortcode'], 'abn123')
