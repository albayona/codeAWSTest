
class SimplePost:
    def __init__(self, link):
        self.link = link

    def attrs_list(self):
        return [(v, k) for v, k in self.__dict__.items()]

    def __str__(self):
        return  '' + self.link