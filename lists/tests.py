from django.test import TestCase
# from django.urls import resolve
# from django.http import HttpRequest
# from .views import home_page


# Create your tests here.
class HomePageTestCase(TestCase):


    # def test_root_url_resolves_to_home_page_view(self):
    """
    This test was rolled in the template check test
    """
        # found = resolve('/')
        # self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        This is unwieldy, so replace with the self.client.get('/')
        The old version created a http response and fed it to the view
        The new version just feeds the url and checks for correct html output
        """

        # request = HttpRequest()  # take response
        # response = home_page(request)  # use response as argument to the view
        # html = response.content.decode('utf8')  # take the html response from the view and parse it
        # self.assertTrue(html.startswith('<!DOCTYPE html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        # self.assertTrue(html.endswith('</html>'))

        response = self.client.get('/')  # get the client response for this url
        html = response.content.decode('utf8')  # get the html

        self.assertTemplateUsed(response, 'html.html')

