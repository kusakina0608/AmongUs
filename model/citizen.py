import random


class Citizen:
    def __init__(self, identifier):
        self.identifier = identifier

    def get_identifier(self):
        return self.identifier

    def vote(self, candidates, weight):
        idx = candidates.index(self.identifier)
        candidates.pop(idx)
        weight.pop(idx)
        victim = random.choices(candidates, weight)
        return victim[0]
