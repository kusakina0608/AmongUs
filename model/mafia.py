import random

from . import Citizen


class Mafia(Citizen):
    def __init__(self, identifier):
        super().__init__(identifier)

    def murder_vote(self, citizen):
        victim = random.choice(citizen)
        return victim
