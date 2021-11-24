from mafia.game_manager import GameManager

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

num_player = 12
num_mafia = 1
num_police = 0
num_medic = 0

weight_diff = 1.0

max_revoting = 3

# 의사 수에 따른 시민의 승률
if __name__ == '__main__':
    x = [i for i in range(12)]
    y = []
    for num_medic in x:
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
    d = pd.DataFrame(data={'number of medic': x, 'win rate': y})
    print(d)
    sns.barplot(data=d, x="number of medic", y="win rate")
    plt.ylim(0, 1)
    plt.show()
