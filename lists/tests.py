from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from lists.models import Item

class HomePageTest(TestCase): 
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')  
        self.assertTemplateUsed(response, 'home.html')
    
    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text':'New item'})
 
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, "New item")

    def test_redirect_after_post(self):
        response = self.client.post('/', data={'item_text':'New item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_save_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_can_display_all_items(self):
        Item.objects.create(text = 'item 1')
        Item.objects.create(text = 'item 2')

        response = self.client.get('/')

        self.assertIn('item 1', response.content.decode())
        self.assertIn('item 2', response.content.decode())

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