import os
import configparser
import json
import neural

if __name__ == '__main__':
    if not os.path.exists('config.ini'):
        raise FileNotFoundError('There\'s no config.ini file')
    config = configparser.ConfigParser()
    config.read('config.ini')
    inputs = int(config.get('DEFAULT', 'width')) * int(config.get('DEFAULT',
                                                                  'height'))
    hidden = int(config.get('DEFAULT', 'hidden'))
    alphabet = config.get('DEFAULT', 'alphabet')
    rate = float(config.get('DEFAULT', 'learning_rate'))
    outputs = len(alphabet)

    net = neural.neuralNetwork(alphabet, inputs, hidden, outputs, rate)

    filename = config.get('NET', 'file')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            net.restore(data)
    else:
        net.save()
