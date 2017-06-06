import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras.models import model_from_json
from keras.optimizers import SGD, RMSprop, Adadelta
from keras.metrics import binary_accuracy

import matplotlib.pyplot as plt

import ast


class NeuralNetwork(object):
    @staticmethod
    def train_model(data_x, data_y):
        model = Sequential()

        dummy_y = np_utils.to_categorical(data_y)

        model.add(Dense(input_dim=data_x.shape[1], units=36, activation='tanh'))
        model.add(Dense(units=100, activation='tanh'))
        model.add(Dense(units=dummy_y.shape[1], activation='softmax'))

        rms_prop = RMSprop(lr=0.0003, decay=0.000003)

        model.compile(optimizer=rms_prop, loss='mean_squared_error',
                      metrics=['accuracy', binary_accuracy])
        model.fit(data_x, dummy_y, epochs=20, shuffle=False, batch_size=1, validation_split=0.2)

        return model

    @staticmethod
    def shuffle_in_unison(a, b):
        assert len(a) == len(b)
        shuffled_a = np.empty(a.shape, dtype=a.dtype)
        shuffled_b = np.empty(b.shape, dtype=b.dtype)
        permutation = np.random.permutation(len(a))
        for old_index, new_index in enumerate(permutation):
            shuffled_a[new_index] = a[old_index]
            shuffled_b[new_index] = b[old_index]

        return shuffled_a, shuffled_b

    @staticmethod
    def prepare_data(input_positive_samples, input_negative_samples):
        """
        :param input_positive_samples:
        :param input_negative_samples:
        :return:
        """
        positive_samples = input_positive_samples

        positive_tags = np.ones(np.shape(positive_samples)[0])

        negative_samples = input_negative_samples

        negative_tags = np.zeros(np.shape(negative_samples)[0])

        test_sample_size = int(positive_samples.__len__() * 0.95)

        positive_samples_train, positive_samples_test = np.split(positive_samples, [test_sample_size], axis=0)
        positive_tags_train, positive_tags_test = np.split(positive_tags, [test_sample_size], axis=0)

        negative_samples_train, negative_samples_test = np.split(negative_samples, [test_sample_size], axis=0)
        negative_tags_train, negative_tags_test = np.split(negative_tags, [test_sample_size], axis=0)

        train_samples = np.concatenate((positive_samples_train[:], negative_samples_train[:]))
        train_tags = np.concatenate((positive_tags_train[:], negative_tags_train[:]))

        train_samples, train_tags = shuffle_in_unison(train_samples, train_tags)

        return train_samples, train_tags, positive_samples_test, negative_samples_test

    @staticmethod
    def save_model(model):
        # serialize model to JSON
        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights("model.h5")

    @staticmethod
    def load_model(json_path, weights_path):
        # load json and create model
        json_file = open(json_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        # loaded_model.load_weights(weights_path)

        return loaded_model

    def run_nn_solution(self, input_positive_samples, input_negative_samples):
        train_samples, train_tags, positive_samples_test, negative_samples_test = prepare_data(input_positive_samples,
                                                                                               input_negative_samples)

        model = self.train_model(train_samples, train_tags)

        print 'positive results :'
        print model.predict_proba(positive_samples_test)

        print 'negative results :'
        print model.predict_proba(negative_samples_test)

np.random.seed(1337)  # for reproducibility


def shuffle_in_unison(a, b):
    assert len(a) == len(b)
    shuffled_a = np.empty(a.shape, dtype=a.dtype)
    shuffled_b = np.empty(b.shape, dtype=b.dtype)
    permutation = np.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
    return shuffled_a, shuffled_b


def read_file(path):
    output = []

    with open(path, "r") as positive_file:
        lines = positive_file.readlines()

        for line in lines:
            sample = ast.literal_eval(line)
            output.append(sample)

    return np.array(output)


def add_features(samples):
    # input_times, input_keystrokes_num = np.split(samples, 2, axis=1)

    # mean_time_per_keystroke = np.true_divide(input_times, input_keystrokes_num)

    # times_squared = np.square(input_times)

    # keystrokes_num_squared = np.square(input_keystrokes_num)

    # samples = np.concatenate((samples, mean_time_per_keystroke), axis=1)

    # samples = np.concatenate((samples, times_squared), axis=1)

    # samples = np.concatenate((samples, keystrokes_num_squared), axis=1)

    return samples


def prepare_data(input_positive_samples, input_negative_samples):
    """
    :param input_positive_samples:
    :param input_negative_samples:
    :return:
    """
    positive_samples = input_positive_samples

    positive_tags = np.ones(np.shape(positive_samples)[0])

    negative_samples = input_negative_samples

    negative_tags = np.zeros(np.shape(negative_samples)[0])

    test_sample_size = int(positive_samples.__len__() * 0.95)

    positive_samples_train, positive_samples_test = np.split(positive_samples, [test_sample_size], axis=0)
    positive_tags_train, positive_tags_test = np.split(positive_tags, [test_sample_size], axis=0)

    negative_samples_train, negative_samples_test = np.split(negative_samples, [test_sample_size], axis=0)
    negative_tags_train, negative_tags_test = np.split(negative_tags, [test_sample_size], axis=0)

    train_samples = np.concatenate((positive_samples_train[:], negative_samples_train[:]))
    train_tags = np.concatenate((positive_tags_train[:], negative_tags_train[:]))

    train_samples, train_tags = shuffle_in_unison(train_samples, train_tags)

    return train_samples, train_tags, positive_samples_test, negative_samples_test


def run_nn_solution(input_positive_samples, input_negative_samples):
    train_samples, train_tags, positive_samples_test, negative_samples_test = prepare_data(input_positive_samples,
                                                                                           input_negative_samples)

    model = NeuralNetwork.train_model(train_samples, train_tags)

    print 'positive results :'
    print model.predict_proba(positive_samples_test)

    print 'negative results :'
    print model.predict_proba(negative_samples_test)

    save_model(model)

    model = load_model("model.json", "model.h5")

    model.compile(optimizer='rmsProp', loss='mean_squared_error',
                  metrics=['accuracy', 'binary_accuracy'])

    print "Loaded model: "
    print model.predict_proba(positive_samples_test)


def save_model(model):
    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")


def load_model(json_path, weights_path):
    # load json and create model
    json_file = open(json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(weights_path)

    return loaded_model


features = ['punc', 'speed', 'backspace']

positive_samples = np.array([])
negative_samples = np.array([])

for feature in features:
    positive_file = read_file('./{}-positive.txt'.format(feature))
    print feature.upper()
    print positive_file
    negative_file = read_file('./{}-negative.txt'.format(feature))
    if positive_samples.shape[0] == 0:
        positive_samples = positive_file
        negative_samples = negative_file
    else:
        positive_samples = np.concatenate((positive_samples, positive_file), axis=1)
        negative_samples = np.concatenate((negative_samples, negative_file), axis=1)

print positive_samples[0]

a = NeuralNetwork()

a.run_nn_solution(positive_samples, negative_samples)



# input_positive_samples = positive_samples[input_positive_samples[:,0] < 15000]
# input_negative_samples = negative_samples[input_negative_samples[:,0] < 15000]
#
# input_positive_samples = add_features(input_positive_samples)
# input_negative_samples = add_features(input_negative_samples)
#
# fig, ax = plt.subplots()
# ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
# # for name, group in groups:
#
# ax.plot(input_positive_samples[:,0], input_positive_samples[:,2], marker='o', color='g', linestyle='', ms=12, label="positives")
# ax.plot(input_negative_samples[:,0], input_negative_samples[:,2], marker='o', color='r', linestyle='', ms=12, label="negatives")
#
#
#
#
# ax.legend()
#
# plt.show()

# def twoD_Gaussian((x, y), amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
#     xo = float(xo)
#     yo = float(yo)
#     a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
#     b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
#     c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
#     g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo)
#                             + c*((y-yo)**2)))
#     return g.ravel()
#
# x = np.linspace(0, 586, 587)
# y = np.linspace(0, 586, 587)
# x, y = np.meshgrid(x, y)
#
# data = twoD_Gaussian((x, y), 3, 7500, 100, 3000, 40, 0, 10)
#
# initial_guess = (3, 7500, 100, 3000, 40, 0, 10)
#
# popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y), , p0=initial_guess)
#
# plt.figure()
# plt.imshow(data.reshape(587, 587))
# plt.colorbar()
#
# # data_fitted = twoD_Gaussian((x, y), *popt)
#
# fig, ax = plt.subplots(1, 1)
# ax.hold(True)
# # ax.imshow(data_noisy.reshape(201, 201), cmap=plt.cm.jet, origin='bottom',
# #     extent=(x.min(), x.max(), y.min(), y.max()))
# ax.contour(x, y, data.reshape(587, 587), 8, colors='w')
# plt.show()

# train_samples, train_tags, positive_samples_test, negative_samples_test = prepare_data(input_positive_samples, input_negative_samples)
#
# clf = svm.NuSVC(kernel='poly', degree=3, probability=True)
# clf.fit(train_samples, train_tags)
#
# print 'positive results :'
# print clf.predict(positive_samples_test)
#
# print 'negative results :'
# print clf.predict(negative_samples_test)
