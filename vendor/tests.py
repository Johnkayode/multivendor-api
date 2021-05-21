from django.test import TestCase
from vendor.models import CustomUser

from rest_framework.test import APITestCase, APIClient

from vendor.models import CustomUser


class TestVendor(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/vendors/'
        params = {
            "user":{
                "email": "newtonjohn043@gmail.com",
                "first_name": "test",
                "last_name": "testing",
                "password": "test123"
            },
            "shop_name" : "Test Shop",
            "description" : "My Test Shop",
            "phone_number" : "09034727466"

        }
        response = self.client.post(self.url, params, format='json')
        self.confirmation_code = dict(response.data['user'])['confirmation_code']
        self.assertEqual(response.status_code, 201, f'Expected Response code 201, received {response.status_code} instead.')
        self.token = None
        
    def test_account_vendor(self):
        # Test unconfirmed login
        params = {
            "email": "newtonjohn043@yahoo.com",
            "password": "test123"
        }
        response = self.client.post(self.url + "signin/", params, format='json')
        self.assertEqual(response.status_code, 400, f'Expected Response code 400, received {response.status_code} instead.')
        
        # test confirm account
        params = {
            "confirmation_code": self.confirmation_code
        }
        response = self.client.post(self.url + "confirm-account/", params, format='json')
        self.assertEqual(response.status_code, 200, f'Expected Response code 200, received {response.status_code} instead.')
        
        #test already confirmed account
        params = {
            "confirmation_code": self.confirmation_code
        }
        response = self.client.post(self.url + "confirm-account/", params, format='json')
        self.assertEqual(response.status_code, 400, f'Expected Response code 400, received {response.status_code} instead.')

        #test fake login
        params = {
            "email": "newton@yahoo.com",
            "password": "test123"
        }
        response = self.client.post(self.url + "signin/", params, format='json')
        self.assertEqual(response.status_code, 400, f'Expected Response code 400, received {response.status_code} instead.')

        #test login
        params = {
            "email": "newtonjohn043@gmail.com",
            "password": "test123"
        }
        response = self.client.post(self.url + "signin/", params, format='json')
        #self.token = response.data['token']
        print(response.data)
        self.assertEqual(response.status_code, 200, f'Expected Response code 200, received {response.status_code} instead.')
    

    def test_get_vendors(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, f'Expected Response code 200, received {response.status_code} instead.')
        print(self.confirmation_code)

    