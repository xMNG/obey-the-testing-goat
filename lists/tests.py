from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from .views import home_page


# Create your tests here.
class HomePageTestCase(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  # take response
        response = home_page(request)  # use response as argument to the view
        html = response.content.decode('utf8')  # take the html response from the view and parse it
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))