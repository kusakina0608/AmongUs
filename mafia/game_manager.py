from model import *


class GameManager:
    def __init__(self, num_player, num_mafia, num_police, num_medic, weight_diff, max_revoting, debug = False):
        if num_player < num_mafia + num_police + num_medic:
            raise Exception("numPlayer error")
        self.date = 1
        self.debug = debug

        self.num_player = num_player
        self.num_mafia = num_mafia
        self.num_police = num_police
        self.num_medic = num_medic

        self.weight_diff = weight_diff
        self.max_revoting = max_revoting

        # 시민을 생성
        self.players = [Citizen(i + 1) for i in range(self.num_player)]
        self.weight = [1.0 for i in range(self.num_player)]

        # 경찰 수사기록
        self.suspect = set([])
        self.innocent = set([])

        # 마피아 선정
        for _ in range(self.num_mafia):
            mafia_id = random.choice(self.get_citizen_id_list())
            self.players[self.get_id_list().index(mafia_id)] = Mafia(mafia_id)
            if debug:
                print(mafia_id, "번 플레이어가 마피아로 선정되었습니다.")

        # 경찰 선정
        for _ in range(self.num_police):
            police_id = random.choice(self.get_citizen_id_list())
            self.players[self.get_id_list().index(police_id)] = Police(police_id)
            if debug:
                print(police_id, "번 플레이어가 경찰로 선정되었습니다.")

        # 의사 선정
        for _ in range(self.num_medic):
            medic_id = random.choice(self.get_citizen_id_list())
            self.players[self.get_id_list().index(medic_id)] = Medic(medic_id)
            if debug:
                print(medic_id, "번 플레이어가 의사로 선정되었습니다.")

    def start(self):
        while True:
            self.daytime()
            if self.num_mafia == 0:
                if self.debug:
                    print("모든 마피아가 사망하여 시민 팀이 승리하였습니다.")
                return True
            if self.num_mafia >= self.num_player - self.num_mafia:
                if self.debug:
                    print("마피아 팀이 승리하였습니다.")
                return False
            self.night()
            if self.num_mafia >= self.num_player - self.num_mafia:
                if self.debug:
                    print("마피아 팀이 승리하였습니다.")
                return False
            self.date += 1

    def daytime(self):
        if self.debug:
            print("\n[", self.date, "일차 낮 ]")
        self.investigate()
        if self.debug:
            print("weight:", end="")
            for i in range(len(self.players)):
                print("(", self.players[i].get_identifier(), ":", self.weight[i], ") ", sep="", end="")
            print()
        self.voting()
        if self.debug:
            print(self.get_id_list())
        pass

    def night(self):
        if self.debug:
            print("\n[", self.date, "일차 밤 ]")
        victim = self.murder_voting()
        targets = self.treatment()
        if victim in targets:
            if self.debug:
                print(victim, "번 플레이어가 마피아에게 지목당하였으나 살아남았습니다.")
        else:
            if self.debug:
                print(victim, "번 플레이어가 마피아에게 살해당하였습니다.")
            idx = self.get_id_list().index(victim)
            self.eliminate(idx)
        if self.debug:
            print(self.get_id_list())
        pass

    def investigate(self):
        if self.num_police > 0:
            for player in self.players:
                if player.__class__ == Police:
                    result = player.detect(self.get_id_list())
                    if result == -1:
                        continue
                    idx = self.get_id_list().index(result)
                    if self.players[idx].__class__ == Mafia:
                        if self.debug:
                            print("경찰이", result, "번 플레이어가 마피아인 것을 밝혀냈습니다.")
                        self.suspect.add(result)
                        self.weight[idx] += self.weight_diff
                    else:
                        if self.debug:
                            print("경찰이", result, "번 플레이어가 시민인 것을 밝혀냈습니다.")
                        self.innocent.add(result)

            for player in self.players:
                if player.__class__ == Police:
                    player.update_info(self.suspect, self.innocent)

    def treatment(self):
        result = []
        if self.num_medic > 0:
            for player in self.players:
                if player.__class__ == Medic:
                    result.append(player.heal(self.get_id_list()))
        return list(set(result))

    def voting(self):
        for i in range(self.max_revoting):
            if self.debug:
                print(i + 1, "번째 투표를 시작합니다.")
            result = {key: 0 for key in self.get_id_list()}
            for player in self.players:
                result[player.vote(self.get_id_list(), self.weight.copy())] += 1
            elected = [k for k, v in result.items() if max(result.values()) == v]
            if len(elected) == 1:
                if self.debug:
                    print(elected[0], "번 플레이어가 투표로 사망하였습니다.")
                idx = self.get_id_list().index(elected[0])
                self.eliminate(idx)
                return
            if self.debug:
                print("동점자가 발생하여 재투표를 실시합니다.")
        if self.debug:
            print("재투표 횟수 초과로 사망자 투표가 부결되었습니다.")

    def murder_voting(self):
        candidates = self.get_innocent_citizen_id_list()
        while True:
            result = {key: 0 for key in candidates}
            for player in self.players:
                if player.__class__ == Mafia:
                    result[player.murder_vote(candidates)] += 1
            elected = [k for k, v in result.items() if max(result.values()) == v]
            if len(elected) == 1:
                return elected[0]
            candidates = elected

    def eliminate(self, idx):
        if self.players[idx].__class__ == Mafia:
            self.num_mafia -= 1
        elif self.players[idx].__class__ == Police:
            self.num_police -= 1
        elif self.players[idx].__class__ == Medic:
            self.num_medic -= 1
        self.num_player -= 1
        self.players.pop(idx)
        self.weight.pop(idx)

    def get_id_list(self):
        return [player.get_identifier() for player in self.players]

    def get_citizen_id_list(self):
        return [player.get_identifier() for player in filter(lambda x: x.__class__ == Citizen, self.players)]

    def get_innocent_citizen_id_list(self):
        return [player.get_identifier() for player in filter(lambda x: x.__class__ != Mafia, self.players)]
