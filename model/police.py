import random

from . import Citizen


class Police(Citizen):
    def __init__(self, identifier):
        super().__init__(identifier)
        self.suspect = set([])
        self.innocent = set([identifier])

    def detect(self, survivors):
        # 생존자 중에서 이미 수사한 사람을 제외한 한명을 선택
        suspect = set(survivors) - self.suspect - self.innocent
        if suspect:
            suspect = random.choice(list(suspect))
            return suspect
        return -1

    def update_info(self, suspect, innocent):
        self.suspect = self.suspect | suspect
        self.innocent = self.innocent | innocent
