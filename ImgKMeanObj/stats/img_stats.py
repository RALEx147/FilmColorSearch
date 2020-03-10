'''
The class contains the data of img k-means cluster
'''


class img_stats:

    def __init__(self, color_info):
        # self.film = film
        # self.begin_time = begin_time
        # self.end_time = end_time
        self.color_info = sorted(color_info, reverse=True)

    # def __str__(self):
    #     return self.color_info

    def print_info(self):
        for i in self.color_info:
            print(i)
