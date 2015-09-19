import urllib2
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from mock import patch
from app.models import Product

mock_post_urlopen_read = '''<html>
<head>
<head>
<body>
	<img width="145" height="276" data-zoom-url="http://i2.rozetka.ua/goods/852861/record_852861554.jpg" id="base_image" name="base_image" itemprop="image" title="Haircut machine ZELMER ZHC 39012 (39Z012)" alt="Haircut machine ZELMER ZHC 39012 (39Z012)" src="http://i1.rozetka.ua/goods/852861/record_852861596.jpg">
	<div name="prices_active_element_original">
		<span itemprop="price">768</span>
	</div>
</body>
</html>'''


def mock_urlopen_page_not_found(*args, **kwargs):
    raise urllib2.HTTPError('', 404, 'Not found', None, None)


def mock_urlopen_invalid_url(*args, **kwargs):
    raise ValueError('Invalid url')


def mock_urlopen_site_is_not_available(*args, **kwargs):
    raise urllib2.URLError('[Errno 11004] getaddrinfo failed')


class AddProductViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    @patch('app.views.urllib2.urlopen')
    def test_post(self, urlopen):
        urlopen.return_value.read.return_value = mock_post_urlopen_read

        response = self.client.post(reverse('home'), data={'url': 'http://bt.rozetka.com.ua/zelmer2-39z012/p267660/'})
        self.assertEqual(response.status_code, 302)
        products = Product.objects.all()
        self.assertEqual(len(products), 1)
        product = products[0]
        self.assertEqual(product.title, 'Haircut machine ZELMER ZHC 39012 (39Z012)')
        self.assertEqual(product.price, 768.0)
        self.assertEqual(product.image, '/media\\record_852861596.jpg')

    @patch('app.views.urllib2.urlopen', side_effect=mock_urlopen_page_not_found)
    def test_post_page_not_found(self, urlopen):
        response = self.client.post(reverse('home'), data={'url': 'http://bt.rozetka.com.ua/incorrect-url/'})
        self.assertEqual(response.status_code, 404)

    @patch('app.views.urllib2.urlopen', side_effect=mock_urlopen_invalid_url)
    def test_post_invalid_url(self, urlopen):
        response = self.client.post(reverse('home'), data={'url': 'invalid-url'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Invalid url')

    @patch('app.views.urllib2.urlopen', side_effect=mock_urlopen_site_is_not_available)
    def test_post_site_is_not_available(self, urlopen):
        response = self.client.post(reverse('home'), data={'url': 'http://nosite.loc/'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Site is not available')

