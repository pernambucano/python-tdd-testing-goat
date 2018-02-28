from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')



        # User invited to use the To-DO

        # User types "It's on"

        # User hits enter, and "It's on" appears on the screen

        # User enters new text, "Oh Yeah"

        # Page updated showing both texts

        # Page generates unique url

        # User visits unique url, and every both todos are there

        # User finished flow

if __name__ == "__main__":
    unittest.main(warnings='ignore')
