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

plt.plot([x * 100 for x in range(len(bots))], bots)
plt.ylabel("Bots")
plt.savefig(f'./stats/charts/{filename}_bots.png')
plt.close()

plt.plot([x * 100 for x in range(len(deaths))], deaths, label = 'Deaths')
plt.plot([x * 100 for x in range(len(born))], born, label = 'Born')
plt.legend()
plt.savefig(f'./stats/charts/{filename}_deaths_born.png')
plt.close()

plt.plot([x * 100 for x in range(len(green))], green, label = 'Green', color = 'green')
plt.plot([x * 100 for x in range(len(blue))], blue, label = 'Blue', color = 'blue')
plt.legend()
plt.savefig(f'./stats/charts/{filename}_green_blue.png')
plt.close()

plt.plot([x * 100 for x in range(len(aggressiveness))], aggressiveness)
plt.ylabel("Aggressiveness")
plt.savefig(f'./stats/charts/{filename}_aggressiveness.png')
plt.close()

plt.plot([x * 100 for x in range(len(energy))], energy)
plt.ylabel("Energy")
plt.savefig(f'./stats/charts/{filename}_energy.png')
plt.close()
    