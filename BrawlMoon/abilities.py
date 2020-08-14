class Ability:
    def __init__(self, data):
        self.name = data.pop('name')
        self.id = data.pop('id')

    def __repr__(self):
        return self.name


class Gadget(Ability):
    pass


class StarPower(Ability):
    pass
