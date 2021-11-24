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

# 경찰 수와 가중치에 따른 시민의 승률
if __name__ == '__main__':
    x = [(i + 1)/10 for i in range(100)]
    y = []
    num_police_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for num_police in num_police_list:
        local_y = []
        for weight_diff in x:
            citizen_win = 0
            mafia_win = 0
            for i in range(10):
                gm = GameManager(num_player, num_mafia, num_police, num_medic, weight_diff, max_revoting, False)
                result = gm.start()
                if result:
                    citizen_win += 1
                else:
                    mafia_win += 1
            local_y.append(citizen_win / (mafia_win + citizen_win))
        y.append(local_y)

    sns.set(style='darkgrid')
    data = []
    xx = []
    yy = []
    zz = []
    print(data)
    for num_police in num_police_list:
        xx += x
        yy += y[num_police - 1]
        zz += [num_police for _ in range(len(x))]
    data = {'weight': xx, 'win rate': yy, 'number of police': zz}
    d = pd.DataFrame(data=data)
    d_wide = d.pivot('number of police', 'weight', 'win rate')
    print(d_wide)
    sns.lineplot(data=d, x="number of police", y="win rate")
    plt.ylim(0, 1)
    plt.show()
