
import os
import urllib
import urllib2
from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from BeautifulSoup import BeautifulSoup
from mocking.settings import BASE_DIR
from models import Product


class AddProductView(View):
    def get(self, request):
        return render(request, 'add.html', {})

    def post(self, request):
        url = request.POST['url']
        try:
            response = urllib2.urlopen(url, timeout=300)
        except urllib2.HTTPError as e:
            if e.code == 404:
                raise Http404('Product not found')
            raise e
        except ValueError as e:
            return HttpResponseBadRequest('Invalid url')
        except urllib2.URLError as e:
            return HttpResponseBadRequest('Site is not available')

        html = response.read()
        response.close()
        soup = BeautifulSoup(html)
        image = soup.find('img', {'id': 'base_image'})
        image_src = image['src']
        image_name = image['src'].split('/')[-1]
        title = image['title']
        my_image_path = os.path.join('media', image_name)
        image_my_src = os.path.join(BASE_DIR, my_image_path)
        urllib.urlretrieve(image_src, image_my_src)
        price = soup.find('div', {'name': 'prices_active_element_original'}).find('span', {'itemprop': 'price'}).text

        product = Product(title=title, image='/{0}'.format(my_image_path), price=float(price))
        product.save()

        return HttpResponseRedirect('/list/')


class ListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'list.html', {'products': products})


class ProductView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, 'product.html', {'product': product})
