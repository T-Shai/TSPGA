from TSPGen import *

import matplotlib.pyplot as plt
import matplotlib.animation as animation

WIDHT = 10000
HEIGHT = 10000
POP_SIZE = 1000
MUT_CHANCE = 0.03
nCities = 20
pSpeed = 1

cities = cities = [City(random.randint(0, WIDHT), random.randint(0, WIDHT)) for _ in range(nCities)]
g = TSPGen(cities, POP_SIZE, MUT_CHANCE)
xsp = list()
ysp = list()
for city in cities :
    xsp.append(city._x)
    ysp.append(city._y)

fig = plt.figure()
plt.title("TSPGen by T-Shai") 
line,  = plt.plot([],[])
ax = fig.add_subplot(111)
plt.xlim(0, WIDHT)
plt.ylim(0,HEIGHT)
t = ax.text(1,1, "", fontsize=15)
def init():
    plt.scatter(xsp, ysp)
    return line,

def animate(k):
    for _ in range(pSpeed):
        x = list()
        y = list()
        g.nextGen()
        i = g.getBestIndividual()
        for indx in i._gene:
            x.append(cities[indx]._x)
            y.append(cities[indx]._y)
    line.set_data(x, y)
    t.set_text(f"Generation : {g.getNumberOfGen()}\n best fit : {i.getDistance(cities) : .4f}")
    return line, t

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=1, blit=True, interval=1, repeat=True)

plt.show()
