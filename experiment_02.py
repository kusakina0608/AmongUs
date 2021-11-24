from mafia.game_manager import GameManager

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

num_player = 12
num_mafia = 1
num_police = 1
num_medic = 0

weight_diff = 1.0

max_revoting = 3

# 가중치에 따른 시민의 승률
if __name__ == '__main__':
    x = [(i + 1)/10 for i in range(100)]
    y = []
    for weight_diff in x:
        citizen_win = 0
        mafia_win = 0
        for i in range(1000):
            gm = GameManager(num_player, num_mafia, num_police, num_medic, weight_diff, max_revoting, False)
            result = gm.start()
            if result:
                citizen_win += 1
            else:
                mafia_win += 1
        y.append(citizen_win / (mafia_win + citizen_win))

    sns.set(style='darkgrid')
    d = pd.DataFrame(data={'weight': x, 'win rate': y})
    print(d)
    sns.lineplot(data=d, x="weight", y="win rate")
    plt.ylim(0, 1)
    plt.show()
