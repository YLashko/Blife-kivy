import numpy as np
from matplotlib import pyplot as plt

filename = input()
bots = []
deaths = []
green = []
blue = []
born = []
aggressiveness = []
energy = []
looks = []
turns = []
moves = []
shares = []
with open(f'./stats/files/{filename}.txt', 'r') as file:
    for line in file:
        dic = eval(line)
        bots.append(dic['bots'])
        deaths.append(dic['deaths'])
        green.append(dic['green'])
        blue.append(dic['blue'])
        born.append(dic['born'])
        aggressiveness.append(dic['aggressiveness'])
        energy.append(dic['energy'])
        looks.append(dic['looks'])
        turns.append(dic['turns'])
        moves.append(dic['moves'])
        shares.append(dic['shares'])

plt.plot([x * 100 for x in range(len(bots))], bots)
plt.ylabel("Bots/cycle")
plt.savefig(f'./stats/charts/{filename}_bots.png')
plt.close()

plt.plot([x * 100 for x in range(len(deaths))], deaths, label = 'Deaths/cycle')
plt.plot([x * 100 for x in range(len(born))], born, label = 'Born/cycle')
plt.legend()
plt.savefig(f'./stats/charts/{filename}_deaths_born.png')
plt.close()

plt.plot([x * 100 for x in range(len(green))], green, label = 'Green/cycle', color = 'green')
plt.plot([x * 100 for x in range(len(blue))], blue, label = 'Blue/cycle', color = 'blue')
plt.legend()
plt.savefig(f'./stats/charts/{filename}_green_blue.png')
plt.close()

plt.plot([x * 100 for x in range(len(aggressiveness))], aggressiveness)
plt.ylabel("Aggressiveness/bot")
plt.savefig(f'./stats/charts/{filename}_aggressiveness.png')
plt.close()

plt.plot([x * 100 for x in range(len(energy))], energy)
plt.ylabel("Energy/bot")
plt.savefig(f'./stats/charts/{filename}_energy.png')
plt.close()

plt.plot([x * 100 for x in range(len(looks))], looks, label = 'Looks/cycle', color = 'green')
plt.plot([x * 100 for x in range(len(moves))], moves, label = 'Moves/cycle', color = 'blue')
plt.plot([x * 100 for x in range(len(turns))], turns, label = 'Turns/cycle', color = 'red')
plt.plot([x * 100 for x in range(len(shares))], shares, label = 'Shares/cycle', color = 'orange')
plt.legend()
plt.savefig(f'./stats/charts/{filename}_actions.png')
plt.close()