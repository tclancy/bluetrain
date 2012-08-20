from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from bluetrain.models import HtmlPage, PageType


class HtmlPageTests(TestCase):
    fixtures = ['pagetypes.json', 'pages.json']

    def setUp(self):
        self.home = HtmlPage.objects.get(slug='home')
        self.level_one = HtmlPage(title='Level One',
            slug='l1',
            content='x',
            parent=self.home,
            page_type=PageType.objects.get(pk=PageType.NORMAL_PAGE)
        )
        self.level_one.save()
        self.client = Client()

    def test_page_creation(self):
        self.assertEqual(3, HtmlPage.objects.count())
        level_two = HtmlPage(title='Level Two',
            slug='l2',
            content='x',
            parent=self.level_one,
            page_type=PageType.objects.get(pk=PageType.NORMAL_PAGE)
        )
        level_two.save()
        self.assertEqual(4, HtmlPage.objects.count())

        for slug in ['home', 'l1', 'l2']:
            self.assertTrue(self._test_url(reverse('pages_display', args=[slug])))

    def _test_url(self, url, expected_status_code=200):
        response = self.client.get(url)
        return (expected_status_code == response.status_code)
