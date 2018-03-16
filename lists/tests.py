from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from lists.models import Item, List

class HomePageTest(TestCase): 
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')  
        self.assertTemplateUsed(response, 'home.html') 

class ListAndItemModelsTest(TestCase):
    
    def test_saving_and_retrieving_item(self):
        list_ = List()
        list_.save()  

        first_item = Item()
        first_item.text = "First item"
        first_item.list = list_  
        first_item.save()

        second_item = Item()
        second_item.text = "Second Item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_objects = Item.objects.all()
        self.assertEqual(saved_objects.count(), 2)

        self.assertEqual(saved_objects[0].text, "First item")
        self.assertEqual(saved_objects[0].list, list_)
        self.assertEqual(saved_objects[1].text, "Second Item") 
        self.assertEqual(saved_objects[1].list, list_) 

class ListViewTest(TestCase):

    def test_can_display_only_items_for_this_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text = 'item 1', list=correct_list)
        Item.objects.create(text = 'item 2', list=correct_list)
        wrong_list = List.objects.create()
        Item.objects.create(text ='item 3', list=wrong_list)
        Item.objects.create(text ='item 4', list=wrong_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'item 3')
        self.assertNotContains(response, 'item 4')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/') 
        self.assertTemplateUsed(response, 'lists.html')

class NewListTest(TestCase): 

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text':'New item'})
 
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, "New item")

    def test_redirect_after_post(self): 
        response = self.client.post('/lists/new', data={'item_text':'New item'})
        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        wrong_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
        data={'item_text':'New Item'}) 
        
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'New Item')
        self.assertEqual(item.list, correct_list)

    def test_can_save_a_POST_and_redirects_to_list_view(self):
        correct_list = List.objects.create()
        wrong_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': 'New Item'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

