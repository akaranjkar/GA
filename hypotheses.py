import random
from data_reader import DataReader

class Hypotheses:
    """Class for hypotheses"""

    def __init__(self, ruleset_size, bitstring_size,attributes):
        self.ruleset_size = ruleset_size
        self.bitstring_size = bitstring_size
        self.attributes = attributes
        self.bitstring = None
        self.fitness_score = 0.0
        self.generate_random_hypotheses()

    def __lt__(self, other):
        return self.fitness_score < other.fitness_score

    def generate_random_hypotheses(self):
        hypotheses = ''
        # for j in range(self.ruleset_size):
        #     hypotheses += ''.join(random.choice('01') for _ in range(self.bitstring_size))
        for i in range(self.ruleset_size):
            for j in range(len(self.attributes)):
                if j != len(self.attributes) - 1:
                    hypotheses += ''.join(random.choice('01') for _ in range(len(self.attributes[j]['values'])))
                else:
                    temp_consequent = '0' * len(self.attributes[j]['values'])
                    random_bit = random.randint(0, len(self.attributes[j]['values']) - 1)
                    temp_consequent = temp_consequent[:random_bit] + '1' + temp_consequent[random_bit+1:]
                    hypotheses += temp_consequent
        self.bitstring = hypotheses

    def mutate(self):
        random_bit = random.randint(0,len(self.bitstring) - 1)
        if self.bitstring[random_bit] == '0':
            self.bitstring= self.bitstring[:random_bit] + '1' + self.bitstring[random_bit+1:]
        else:
            self.bitstring = self.bitstring[:random_bit] + '0' + self.bitstring[random_bit+1:]

    def print_rules(self):
        bitstrings = []
        hypotheses = self.bitstring
        while hypotheses != '':
            bitstrings.append(hypotheses[:self.bitstring_size])
            hypotheses = hypotheses[self.bitstring_size:]
        for bitstring in bitstrings:
            print(self.bitstring_to_rule(bitstring))

    def bitstring_to_rule(self,bitstring):
        antecedent = []
        consequent = []
        for i in range(len(self.attributes)):
            if i != len(self.attributes) - 1: # Antecedent
                temp_antecedent = []
                no_of_bits = len(self.attributes[i]['values'])
                ignore = True
                for j in range(no_of_bits):
                    if bitstring[j] == '1':
                        temp_antecedent.append(self.attributes[i]['attr']
                                               + " = "
                                               + self.attributes[i]['values'][j])
                    else:
                        ignore = False
                if not ignore:
                    temp_antecedent = " V ".join(temp_antecedent)
                    antecedent.append(temp_antecedent)
                bitstring = bitstring[no_of_bits:]
            else: # Consequent
                temp_consequent = []
                no_of_bits = len(self.attributes[i]['values'])
                for j in range(no_of_bits):
                    if bitstring[j] == '1':
                        temp_consequent.append(self.attributes[i]['attr']
                                               + " = "
                                               + self.attributes[i]['values'][j])
                temp_consequent = " V ".join(temp_consequent)
                consequent.append(temp_consequent)
                bitstring = bitstring[no_of_bits:]
        rule = " ^ ".join(antecedent) + " => " + " ^ ".join(consequent)
        return rule

    def valid(self, rule):
        for i in range(len(self.attributes)):
            if i != len(self.attributes) - 1: # Antecedent
                no_of_bits = len(self.attributes[i]['values'])
                if rule[:no_of_bits] == '0' * no_of_bits:
                    return False
                rule = rule[no_of_bits:]
            else: # Consequent
                no_of_bits = len(self.attributes[i]['values'])
                if rule[:no_of_bits] == '0' * no_of_bits or rule[:no_of_bits] == '1' * no_of_bits:
                    return False
                rule = rule[no_of_bits:]
        return True

    def test_rule(self,rule,test):
        if not self.valid(rule):
            return False
        res = bin(int(rule,2) & int(test,2))[2:].zfill(len(rule))
        return self.valid(res)

    def fitness(self,tests):
        correct = 0
        total = len(tests)
        rules = []
        hypotheses = self.bitstring
        while hypotheses != '':
            rules.append(hypotheses[:self.bitstring_size])
            hypotheses = hypotheses[self.bitstring_size:]
        for test in tests:
            classified = False
            for rule in rules:
                classified |= self.test_rule(rule,test)
            if classified:
                correct += 1
        self.fitness_score = (float(correct)/total) ** 2
        return self.fitness_score

    @staticmethod
    def crossover(h1,h2):
        # Single point crossover assuming both hypotheses are of equal length
        crossover_point = len(h1)/2
        h3 = h1[:crossover_point] + h2[crossover_point:]
        h4 = h2[:crossover_point] + h1[crossover_point:]
        return h3,h4


if __name__ == '__main__':
    t = DataReader('tennis-attr.txt', 'tennis-train.txt', 'tennis-test.txt')
    t.read_attr_file()
    t.read_train_file()
    t.read_test_file()
    h = Hypotheses(1, 12, t.attributes)
    h.generate_random_hypotheses()
    h.bitstring = '111111111110'
    h.print_rules()
    print(h.fitness(t.bitstring_test_data))