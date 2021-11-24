from mafia.game_manager import GameManager

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

num_player = 8
num_mafia = 1
num_police = 2
num_medic = 2

weight_diff = 1.0

max_revoting = 3

if __name__ == '__main__':
    citizen_win = 0
    mafia_win = 0
    x = []
    citizen_win_rate = []
    for i in range(1000):
        gm = GameManager(num_player, num_mafia, num_police, num_medic, weight_diff, max_revoting, False)
        result = gm.start()
        if result:
            citizen_win += 1
        else:
            mafia_win += 1
        x.append(i)
        citizen_win_rate.append(citizen_win/(citizen_win + mafia_win))
    print("시민 승리:", citizen_win)
    print("마피아 승리:", mafia_win)

    sns.set(style='darkgrid')
    d = pd.DataFrame(data={'total game': x, 'win rate': citizen_win_rate})
    sns.lineplot(data=d, x="total game", y="win rate")
    plt.ylim(0, 1)
    plt.show()
