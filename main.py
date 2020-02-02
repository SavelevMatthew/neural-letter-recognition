import os
import configparser
import json
import neural
import applogic
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    if not os.path.exists(os.path.join(os.getcwd(), 'config.ini')):
        raise FileNotFoundError('There\'s no config.ini file')
    config = configparser.ConfigParser()
    config.read('config.ini')
    scaled_w = int(config.get('DEFAULT', 'width'))
    scaled_h = int(config.get('DEFAULT', 'height'))
    inputs = scaled_h * scaled_w
    hidden = int(config.get('DEFAULT', 'hidden'))
    alphabet = config.get('DEFAULT', 'alphabet')
    rate = float(config.get('DEFAULT', 'learning_rate'))
    outputs = len(alphabet)
    lc = int(config.get('DEFAULT', 'learning_cycles'))
    train_data = config.get('DEFAULT', 'train_file').replace('/', os.path.sep)

    net = neural.neuralNetwork(alphabet, train_data, inputs, hidden, outputs,
                               rate, lc)

    filename = config.get('NET', 'file')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            net.restore(data)
    else:
        net.retrain()
        net.save()

    win_w = int(config.get('APP', 'width'))
    win_h = int(config.get('APP', 'height'))
    caption = config.get('APP', 'caption')
    app = QApplication(sys.argv)
    window = applogic.Application(win_w, win_h, caption, scaled_w, scaled_h,
                                  net)
    sys.exit(app.exec_())
