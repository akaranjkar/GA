import random
from data_reader import DataReader
from hypotheses import Hypotheses

class GA:
    """Class for genetic algorithm"""

    def __init__(self,p,r,m):
        self.population_size = p
        self.population_replacement = r
        self.mutation_rate = m
        self.population = []
        self.tournament_selection_probability = 0.7
        self.selection_strategy = self.tournament_selection
        self.stopping_criterion = 'iterations'

    def initialize_population(self,ruleset_size,bitstring_size,attributes):
        for i in range(self.population_size):
            self.population.append(Hypotheses(ruleset_size,bitstring_size,attributes))

    def evaluate(self,tests):
        for hypotheses in self.population:
            hypotheses.fitness(tests)

    def roulette_selection(self,count,collection):
        total_fitness = 0.0
        for hypotheses in collection:
            total_fitness += hypotheses.fitness_score
        new_population = []
        i = 0
        while len(new_population) < count:
            hypotheses = collection[i]
            selection_probability = hypotheses.fitness_score / total_fitness
            chance = random.uniform(0.0,1.0)
            if chance <= selection_probability:
                new_population.append(collection[i])
                del collection[i]
            i += 1
            if i >=len(collection):
                i = 0
        return new_population

    def tournament_selection(self,count,collection):
        new_population = []
        while len(new_population) < count:
            h1 = collection[random.randint(0,len(collection)-1)]
            h2 = collection[random.randint(0,len(collection)-1)]
            chance = random.uniform(0.0,1.0)
            if chance <= self.tournament_selection_probability:
                larger = h1 if h1 > h2 else h2
                new_population.append(larger)
                collection.remove(larger)
            else:
                smaller = h1 if h1 < h2 else h2
                new_population.append(smaller)
                collection.remove(smaller)
        return new_population

    def best_hypothesis(self):
        max_fitness = 0.0
        best_hypothesis = None
        for i in range(len(self.population)):
            if self.population[i].fitness_score > max_fitness:
                max_fitness = self.population[i].fitness_score
                best_hypothesis = self.population[i]
        return best_hypothesis

    # TODO
    # def rank_selection(self):
    #     return True,True

    def evolve(self,training_data):
        current_generation = 0
        self.evaluate(training_data)
        i=0
        best=None
        while current_generation < 100:
            new_population = self.selection_strategy((1-self.population_replacement) * self.population_size,
                                                     self.population[:])
            reproduction_set = self.selection_strategy((self.population_replacement * self.population_size),
                                                       self.population[:])
            for i in range(len(reproduction_set)/2):
                child1, child2 = Hypotheses.crossover(reproduction_set[i],reproduction_set[i+1])
                new_population.append(child1)
                new_population.append(child2)
            for i in range(int(len(new_population) * self.mutation_rate * 100)):
                new_population[random.randint(0,len(new_population)-1)].mutate()
            self.population = new_population
            self.evaluate(training_data)
            current_generation += 1
            best = self.best_hypothesis()
            print("Iteration {0}, Fitness {1}".format(i,best.fitness_score))
        best.print_rules

if __name__ == '__main__':
    g = GA(10,0.1,0.1)
    d = DataReader("tennis-attr.txt","tennis-train.txt","tennis-test.txt")
    d.read_attr_file()
    d.read_train_file()
    d.read_test_file()
    g.initialize_population(1,d.bitstring_length,d.attributes)
    g.evolve(d.bitstring_train_data)