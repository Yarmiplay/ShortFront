from django.test import TestCase
from django.urls import reverse
from .models import Links
from .views import homepage, short_redirect

class LinksTests(TestCase):
    def test_create_short_url(self):
        # Define a key and create a short URL
        test_url = "https://ravkavonline.co.il/he/faq#ravkav-online"
        response = self.client.post(f'/create/', data={'url': test_url})
        
        # Check if the creation was successful (status code 200 or appropriate)
        self.assertEqual(response.status_code, 200) 

        # Check if the Links object was created in the database
        self.assertTrue(Links.objects.filter(dest=test_url).exists())


    def test_redirect_short_url(self):
        test_key = "testkey"

        # Create a Link object in the database
        Links.objects.create(key=test_key, dest="https://example.com")

        # Access the short URL to trigger the redirection
        response = self.client.get(f'/s/{test_key}/')

        # Check if the redirection was successful (status code 302 or appropriate)
        self.assertEqual(response.status_code, 302)  

    def test_redirect_non_existing_short_url(self):
        # Access a non-existing short URL
        response = self.client.get(f'/s/non_existing_key/')

        # Check if the response indicates a non-existing short URL (status code 404 or appropriate)
        self.assertEqual(response.status_code, 404)  # Adjust based on your view logic