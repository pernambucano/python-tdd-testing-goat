from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time

MAX_TIME = 10

class NewVisitorTest(LiveServerTestCase):

    

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_text_in_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows]) 
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_TIME:
                    raise e
                time.sleep(0.5) 

    def test_can_start_a_list_and_retrieve_it_later(self):

        # User opens website
        self.browser.get(self.live_server_url)

        # User notices the title contains 'To-Do'
        self.assertIn('To-Do', self.browser.title)

        # User notices the header contains 'To-Do'
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)  

        # User is invited to use the To-DO
        input_text = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_text.get_attribute('placeholder'), 'Please enter a To-Do')

        # User types "It's on"
        input_text.send_keys('It\'s on')

        # User hits enter, and "It's on" appears on the screen
        input_text.send_keys(Keys.ENTER) 
        self.wait_for_text_in_table('1: It\'s on')

        # User enters new text, "Oh Yeah"
        input_text = self.browser.find_element_by_id('id_new_item')
        input_text.send_keys('Oh Yeah')
        input_text.send_keys(Keys.ENTER) 
        self.wait_for_text_in_table('1: It\'s on')
        self.wait_for_text_in_table('2: Oh Yeah') 


    def test_multiple_users_can_start_a_list_at_different_urls(self):
         
        # Paulo wanted to take some notes
        # So, he started a browser
        self.browser.get(self.live_server_url)

        

        # Entered a text containing 'New Item'
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('New Item')
        input_box.send_keys(Keys.ENTER)

        # And saw that the item was indeed there in the format 'N: text'
        self.wait_for_text_in_table('1: New Item')

        # He also saw that he got a new url only for him
        paulo_url = self.browser.current_url
        self.assertRegex(paulo_url, '/lists/.*')


        # Pedro then came and wanted to have his own todo list
        # So he started by opening a browser
        ## We first close Paulo's browser
        self.browser.quit
        self.browser.get(self.live_server_url)

        # Pedro verifies that there's not a sign of Paulo's itens
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('New Item', page_text)

        # Pedro writes his own items
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Pedro\'s new item one')
        input_box.send_keys(Keys.ENTER)

        # And verifies that the text is indeed there
        self.wait_for_text_in_table('1: Pedro\'s new item one')

        # He then gets a new url as well
        pedro_url = self.browser.current_url
        self.assertRegex(pedro_url, '/lists/.*')
        self.assertNotEqual(pedro_url, paulo_url)

        # And this time there are not Paulo's itens too
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('New Item', page_text)
        self.assertIn('Pedro\'s new item one', page_text)





        # Page updated showing both texts

        # Page generates unique url

        # User visits unique url, and every both todos are there

        # User finished flow
 
    
