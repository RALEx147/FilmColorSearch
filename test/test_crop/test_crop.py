from unittest import TestCase
from src.crop.crop import crop
from PIL import Image
class Test(TestCase):
    def test_crop(self):
        '''
        Test method for crop the masked film
        :return:
        '''

        file_name = "Test5.jpg"
        crop(file_name,"Test5_crop.jpg")

