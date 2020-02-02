import neural
import numpy as np
import os

if __name__ == '__main__':
    input_nodes = 784
    hidden_nodes = 100
    output_nodes = 10
    learning_rate = 0.3

    net = neural.neuralNetwork(input_nodes, hidden_nodes, output_nodes,
                               learning_rate)

    with open(os.path.join('mnist_dataset', 'mnist_train_100.csv'), 'r') as f:
        training_data = f.readlines()

    for record in training_data:
        values = record.split(',')

        inputs = (np.asfarray(values[1:]) / 255.0 * 0.99) + 0.01

        targets = np.zeros(output_nodes) + 0.01
        targets[int(values[0])] = 0.99

        net.train(inputs, targets)
    net.save()

    with open(os.path.join('mnist_dataset', 'mnist_test_10.csv'), 'r') as f:
        test_data = f.readlines()

    success_board = []
    for record in test_data:
        values = record.split(',')

        inputs = (np.asfarray(values[1:]) / 255.0 * 0.99) + 0.01
        correct = int(values[0])

        outputs = net.query(inputs)
        label = np.argmax(outputs)
        print('Answer: {0}; Correct: {1}'.format(label, correct))
        success_board.append(1 if label == correct else 0)

    success = np.asarray(success_board)
    print('Success in {}%'.format(success.sum() / success.size * 100))
