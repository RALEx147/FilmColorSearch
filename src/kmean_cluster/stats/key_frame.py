'''
The class contains the data of img k-means cluster
'''


class KeyFrame:

    def __init__(self, color_info):
        '''
        Initialize the parameter.
        :param color_info: The color distribution of the current frame
        '''
        self.film_name = None
        self.begin_time = None
        self.end_time = None
        self.color_dist = sorted(color_info, reverse=True)

    def __str__(self):
        return "Film Name: {}\n Time Periods: {} to {}\n Color Distribution:\n {}\n".\
            format(self.film_name,self.begin_time,self.end_time,self.color_dist)

    def print_info(self):
        '''
        test method
        :return:
        '''
        for i in self.color_dist:
            print(i)
