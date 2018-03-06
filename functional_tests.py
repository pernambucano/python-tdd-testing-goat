from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # User opens website
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: It\'s on' for row in rows),
            "New To-Do item was not sucessfully added."
        )

        # User enters new text, "Oh Yeah"
        self.fail('Finish the test!')

        # Page updated showing both texts

        # Page generates unique url

        # User visits unique url, and every both todos are there

        # User finished flow

if __name__ == "__main__":
    unittest.main(warnings='ignore')
