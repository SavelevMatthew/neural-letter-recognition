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

        self.alphabet = alphabet
        self.trained = collections.Counter()

        self.lr = learning_rate

        self.w_ih = numpy.random.normal(0.0, pow(self.hnodes, -0.5),
                                        (self.hnodes, self.inodes))
        self.w_ho = numpy.random.normal(0.0, pow(self.onodes, -0.5),
                                        (self.onodes, self.hnodes))

        self.activation_function = lambda x: special.expit(x)

    def train(self, inputs_list, target_list):
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

    def restore(self, data):
        self.inodes = data.get('inputs')
        self.hnodes = data.get('hiddens')
        self.onodes = data.get('outputs')
        self.lr = data.get('lr')
        self.alphabet = data.get('alphabet')
        self.trained = collections.Counter()
        for s in self.alphabet:
            self.trained[s] += data.get(s)
        self.w_ho = numpy.asfarray(data.get('who'))
        self.w_ih = numpy.asfarray(data.get('wih'))

    def retrain(self):
        pass
