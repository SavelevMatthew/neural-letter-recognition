import numpy
from scipy import special
import json
import collections


class neuralNetwork:
    def __init__(self, alphabet, train_data_file, input_nodes=1,
                 hidden_nodes=1, output_nodes=1, learning_rate=0.3,
                 learning_cycles=2):
        self.inodes = input_nodes
        self.hnodes = hidden_nodes
        self.onodes = output_nodes
        self.data_file = train_data_file
        self.learning_cycles = learning_cycles
        self.alphabet = alphabet
        self.trained = {}
        for s in alphabet:
            self.trained[s] = 0

        self.lr = learning_rate

        self.w_ih = numpy.random.normal(0.0, pow(self.hnodes, -0.5),
                                        (self.hnodes, self.inodes))
        self.w_ho = numpy.random.normal(0.0, pow(self.onodes, -0.5),
                                        (self.onodes, self.hnodes))

        self.activation_function = lambda x: special.expit(x)

    def raw_train(self, inputs_list, target_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(target_list, ndmin=2).T

        h_inputs = numpy.dot(self.w_ih, inputs)
        h_outputs = self.activation_function(h_inputs)

        o_inputs = numpy.dot(self.w_ho, h_outputs)
        o_outputs = self.activation_function(o_inputs)

        o_errors = targets - o_outputs
        h_errors = numpy.dot(self.w_ho.T, o_errors)

        self.w_ho += numpy.dot((o_errors * o_outputs * (1.0 - o_outputs)),
                               numpy.transpose(h_outputs)) * self.lr
        self.w_ih += numpy.dot((h_errors * h_outputs * (1.0 - h_outputs)),
                               numpy.transpose(inputs)) * self.lr

    def train(self, inputs_list, char, base_add=True):
        targets = self.get_target(char)
        self.raw_train(inputs_list, targets)
        if base_add:
            self.trained[char] += 1
            with open(self.data_file, 'a') as f:
                s = char + ', ' + ', '.join(map(self.zeros_to_hundreds,
                                                inputs_list.tolist())) + '\n'
                f.write(s)

    def zeros_to_hundreds(self, s):
        return str(int((s - 0.01) / 0.99 * 255))

    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T

        h_inputs = numpy.dot(self.w_ih, inputs)
        h_outputs = self.activation_function(h_inputs)

        o_inputs = numpy.dot(self.w_ho, h_outputs)
        o_outputs = self.activation_function(o_inputs)

        return o_outputs

    def save(self):
        data = {}
        data['inputs'] = self.inodes
        data['hidden'] = self.hnodes
        data['outputs'] = self.onodes
        data['lr'] = self.lr
        data['alphabet'] = self.alphabet
        for s in self.alphabet:
            data[s] = self.trained[s]
        data['wih'] = self.w_ih.tolist()
        data['who'] = self.w_ho.tolist()
        with open('net.json', 'w+') as f:
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        print('Network saved!')

    def restore(self, data):
        self.inodes = data.get('inputs')
        self.hnodes = data.get('hiddens')
        self.onodes = data.get('outputs')
        self.lr = data.get('lr')
        self.alphabet = data.get('alphabet')
        self.trained = {}
        for s in self.alphabet:
            self.trained[s] = int(data.get(s))
        self.w_ho = numpy.asfarray(data.get('who'))
        self.w_ih = numpy.asfarray(data.get('wih'))

    def retrain(self):
        for _ in range(self.learning_cycles):
            with open(self.data_file, 'r') as f:
                for line in f:
                    parts = line.split(',')
                    char = parts[0]
                    inputs = (numpy.asfarray(parts[1:]) / 255.0 * 0.99) + 0.01
                    self.train(inputs, char, False)

    def get_target(self, char):
        index = self.alphabet.index(char)
        targets = numpy.zeros([len(self.alphabet)]) + 0.01
        targets[index] = 0.99
        return targets
