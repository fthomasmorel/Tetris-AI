import random
import math
import statistics
import time
from operator import itemgetter
from tetris import TetrisApp
from sys import stdout

def createIndividual(size):
    result = []
    for i in range(0, size):
        result.append(random.uniform(-10, 10))
    return result

def individualFromDistribution(average, std):
    result = []
    for i in range(0, size):
        result.append(random.normalvariate(average[i], std[i]))
    return result

def createGeneration(number, size):
    results = []
    for i in range(0, number):
        tmp = createIndividual(size)
        results.append(tmp)
    return results

def generationFromDistribution(number, size, average, std):
    results = []
    for i in range(0, number):
        tmp = individualFromDistribution(average, std)
        results.append(tmp)
    return results

def mutate(x):
    tmp = createIndividual(len(x))
    for i in range(0, len(x)):
        if random.uniform(0, 1) > 0.6:
            x[i] = tmp[i]
    return x

def crossIndivuals(x, y):
    result = []
    for i in range(0, len(x)):
        if random.uniform(0, 1) > 0.5:
            result.append(y[i])
        else:
            result.append(x[i])
    return x

def selectBestIndividuals(scores, number):
    bests = list(reversed(sorted(scores, key=itemgetter(0))))[0:number]
    return list(map(lambda x: x[1], bests))

def fitness(individual, seeds, pieceLimit):
    results = []
    for seed in seeds:
        results.append(TetrisApp(False, seed).run(indiv, pieceLimit))
    return int(sum(results)/len(results))

def computeAverage(population):
    result = list(reduce(lambda i1, i2: [a+b for a,b in zip(i1, i2)], population))
    result = list(map(lambda x: x/len(population), result))
    return result

def computeStandardDeviation(population):
    average = computeAverage(population)
    result = [[] for _ in range(0, len(population[0]))]
    for individual in population:
        for index, weight in enumerate(individual):
            result[index].append(weight)
    result = list(map(lambda weights: statistics.stdev(weights), result))
    return result

survivors_rate = 0.2
pieceLimit = 1000
number = 50
batch = 100
size = 34

generation = createGeneration(number, size)
for iteration in range(0, batch):
    start_time = time.time()
    seeds = []
    for _ in range(0, 5):
        seeds.append(random.randint(0, 100000000))

    print("")
    print("")
    print("--- Batch " + str(iteration) + " ---")
    print("")
    scores = []
    for index, indiv in enumerate(generation):
        message = "\rindiv. " + str(index) + "/" + str(len(generation))
        stdout.write(message)
        stdout.flush()
        scores.append([fitness(indiv, seeds, pieceLimit), indiv])
    print "\n"
    for value in (list(reversed(sorted(scores, key=itemgetter(0))))):
        print(value)
    survivors = selectBestIndividuals(scores, int(len(scores)*survivors_rate))
    print(len(survivors))
    generation = survivors

    average = computeAverage(survivors)
    extra_var_multiplier = max((1.0-iteration/float(batch/2)),0)
    std = list(map(lambda std: std + 0.01 * extra_var_multiplier, computeStandardDeviation(survivors)))

    print ""
    print "time elapsed: ", time.time() - start_time
    print "average: ", average
    print "std: ", std
    print ""

    for individual in generationFromDistribution(number-len(generation), size, average, std):
        generation.append(individual)
