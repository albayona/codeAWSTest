import re
from datetime import datetime

from api.utils.filter_keywords import *


def get_score(description, miles, model, price, year):
    if miles == 0:
        miles = 250000.0

    score = (1000.0 / price) * 3.5 + ((year % 2000.0) / 20.0) * 3.0 + (100000.0 / miles) * 5.0
    for txt in CONS:
        search = re.search(txt, description, re.IGNORECASE)
        if search:
            score -= 2.0
    for txt in PROS:
        search = re.search(txt, description + model, re.IGNORECASE)
        if search:
            score += 1.0

    if score > 100:
        score = score / 100.0

    return score


class DetailedPost:
    def __init__(self, scraped_text: str, description: str, date: datetime, price: float, model: str,
                 place: str, miles: float, link: str, year: int, images: list):
        self.description = description
        self.date = date
        self.price = price
        self.model = model
        self.place = place
        self.miles = miles
        self.link = link
        self.year = year
        self.images = images
        self.score = get_score(description, miles, model, price, year)
        self.scraped_text = scraped_text

    def attrs_list(self):
        return [(v, k) for v, k in self.__dict__.items()]

    def __str__(self):
        attributes_str = ""
        for attr_name, attr_value in vars(self).items():
            attributes_str += f"{attr_name}: {attr_value}\n"
        return attributes_str
