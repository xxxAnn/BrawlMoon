import re


class Brawler:
    def __init__(self, data):
        star_powers = data.pop('starPowers')
        gadges = data.pop('gadgets')

        def camel_to_snake(name):
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

        for k in data.keys():
            snake = camel_to_snake(k)
            setattr(self, snake, data[k])

    def __repr__(self):
        return '\n' + self.name 