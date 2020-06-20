import random
import copy
import math

class City(object):
    """
        City class allows to hold the position and perform distance calculations
    """
    def __init__(self, x : int, y : int):
        self._x = x
        self._y = y

    @staticmethod
    def distance(a , b ):
        """
            Performs pythagorean distance
        """
        return math.sqrt((a._x - b._x)**2 + (a._y - b._y)**2)


class Individual(object):
    """
        Individual class holds genome and fitness score
    """

    def __init__(self, citiesIndx : list):
        """
            random init of gene
        """

        # Shuffling copied index list
        self._gene = citiesIndx
        random.shuffle(self._gene)

        self._fitnessScore = -1 # default value for fitness
        return 

    def getClone(self):
        """
            returns a copy of the current Individual
        """

        return copy.deepcopy(self)

    def calcFitness(self, cities : list):
        """
            Calculate the fitness score with given list of city
        """
        s = 0
        i = 0
        while(i < len(self._gene)-1):
            s += City.distance(cities[self._gene[i]], cities[self._gene[i+1]])
            i += 1
        # print(f"self : {self} s : {s}")
        self._fitnessScore = 1/(s+1)
    
    def getDistance(self, cities):
        s = 0
        i = 0
        while(i < len(self._gene)-1):
            s += City.distance(cities[self._gene[i]], cities[self._gene[i+1]])
            i += 1
        return s

    def mutate(self, MUT_CHANCE):
        if(random.random() < MUT_CHANCE):
            # swaps 2 random elements of the list
            i1 = random.randint(0,len(self._gene)-1)
            i2 = random.randint(0,len(self._gene)-1)
            while(i1 == i2):
                i2 = random.randint(0,len(self._gene)-1)
            self._gene[i1], self._gene[i2] = self._gene[i2], self._gene[i1]

    def __repr__(self):
        return f"gene : {self._gene}\nfitness : {self._fitnessScore}"


class TSPGen(object):
    """
        TSPGen manages the actual genetic algorithm usig Individual
    """

    def __init__(self, cities : list, POP_SIZE : int, MUT_CHANCE : float):

        self._cities = cities
        self.POP_SIZE = POP_SIZE
        self.MUT_CHANCE = MUT_CHANCE
        self._population = [Individual([i for i in range(len(cities))]) for _ in range(POP_SIZE)]
        self._nGen = 0
        self.updateFitness()

    def nextGen(self):
        nwPop = list()
        for _ in range(self.POP_SIZE):
            child = self.pickOne()
            child.mutate(self.MUT_CHANCE)
            nwPop.append(child)
        self._population = nwPop
        self.updateFitness()
        self._nGen += 1
        return

    def updateFitness(self, norm = True):
        s = 0
        for indv in self._population:
            indv.calcFitness(self._cities)
            s+= indv._fitnessScore

        if norm:
            for indv in self._population:
                indv._fitnessScore = indv._fitnessScore/s

    def pickOne(self):
        indx = 0
        r = random.random()
        while(r > 0):
            r = r - self._population[indx]._fitnessScore
            indx += 1
        return self._population[indx-1].getClone()

    def getBestIndividual(self):
        bestInd = None
        bestFit = -1

        for indv in self._population:
            if indv._fitnessScore > bestFit:
                bestFit = indv._fitnessScore
                bestInd = indv
        
        return bestInd

    def getNumberOfGen(self):
        return self._nGen


if __name__ == "__main__":
    cities = [City(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(20)]
    # cities = [City(0,0), City(1,1), City(2,2), City(-7,-7), City(3,3)]
    g = TSPGen(cities, 1000, 0.3)
    while(True):
        g.nextGen()
        print(g.getBestIndividual())


