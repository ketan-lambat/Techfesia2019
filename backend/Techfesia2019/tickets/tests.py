from django.test import TestCase
from django.test import SimpleTestCase
from django.urls  import reverse, resolve
from .views import TicketCreateListView

# Create your tests here.

class TestURLs(SimpleTestCase):
  def test_url_is_resolved(self):
    url = reverse('TicketCreate')
    print(resolve(url))
    self.assertEquals(resolve(url).func, TicketCreateListView)