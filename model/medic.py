import random

from . import Citizen


class Medic(Citizen):
    def __init__(self, identifier):
        super().__init__(identifier)

    def heal(self, survivors):
        target = random.choice(survivors)
        return target
