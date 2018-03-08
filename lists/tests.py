from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

class HomePageTest(TestCase): 
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')  
        self.assertTemplateUsed(response, 'home.html')
    
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text':'New item'})
        self.assertIn('New item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_item(self):
        first_item = Item()
        first_item.text = "First item"
        first_item.save()

        second_item = Item()
        second_item.text = "Second Item"
        second_item.save()

        saved_objects = Item.objects.all()
        self.assertEqual(saved_objects.count(), 2)

        self.assertEqual(saved_objects[0].text, "First item")
        self.assertEqual(saved_objects[1].text, "Second Item")