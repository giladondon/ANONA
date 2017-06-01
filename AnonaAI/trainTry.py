import numpy as np

from keras.models import Sequential
from keras.layers import Input, Dense, Dropout
from keras.layers.pooling import MaxPooling1D
from keras.layers.core import Reshape
from keras.utils import np_utils
from keras.optimizers import SGD, RMSprop, Adadelta

import scipy.optimize as opt

from sklearn import svm

import matplotlib.pyplot as plt

import ast

np.random.seed(1337)  # for reproducibility

def train_model(dataX, dataY):
    model = Sequential()

    dummy_y = np_utils.to_categorical(dataY)

    model.add(Dense(input_dim=dataX.shape[1], output_dim=10, activation='tanh'))
    # model.add(Dropout(p=0.1))
    # model.add(Reshape(target_shape=(5, 5)))
    # model.add(MaxPooling1D(pool_length=2))
    # model.add(Reshape(target_shape=(10,)))
    # model.add(Dense(output_dim=25, activation='tanh'))
    # model.add(Reshape(target_shape=(5, 5)))
    # model.add(MaxPooling1D(pool_length=2))
    # model.add(Reshape(target_shape=(10,)))
    # model.add(Dense(output_dim=10, activation='tanh'))
    # model.add(Dense(output_dim=25, activation='relu'))
    model.add(Dense(output_dim=100, activation='tanh'))
    # model.add(Dense(output_dim=25, activation='linear'))
    model.add(Dense(output_dim=1000, activation='tanh'))
    # model.add(Dense(output_dim=125, activation='linear'))
    # model.add(Dense(output_dim=125, activation='tanh'))
    model.add(Dense(output_dim=dummy_y.shape[1], activation='softmax'))

    sgd = SGD(lr=0.001)

    print("sgd lr = 0.1")
    rmsProp = RMSprop(lr=0.0003, decay=0.000003)

    model.compile(optimizer=rmsProp, loss='mean_squared_error',
                  metrics=['accuracy', 'fmeasure', 'precision', 'recall'])
    model.fit(dataX, dummy_y, nb_epoch=100, shuffle=False, batch_size=1, validation_split=0.2)

    return model

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
            if sample[0] != 0:
                output.append(sample)

    print output
    return np.array(output)

def add_features(samples):
    input_times, input_keystrokes_num = np.split(samples, 2, axis=1)

    mean_time_per_keystroke = np.true_divide(input_times, input_keystrokes_num)

    times_squared = np.square(input_times)

    keystrokes_num_squared = np.square(input_keystrokes_num)

    samples = np.concatenate((samples, mean_time_per_keystroke), axis=1)

    # samples = np.concatenate((samples, times_squared), axis=1)

    # samples = np.concatenate((samples, keystrokes_num_squared), axis=1)

    return samples

def prepare_data(input_positive_samples, input_negative_samples):
    positive_samples = add_features(input_positive_samples)

    positive_tags = np.ones(np.shape(positive_samples)[0])

    negative_samples = add_features(input_negative_samples)

    negative_tags = np.zeros(np.shape(negative_samples)[0])

    positive_samples_train, positive_samples_test = np.split(positive_samples, [positive_samples.__len__() * 0.95], axis=0)
    positive_tags_train, positive_tags_test = np.split(positive_tags, [positive_tags.__len__() * 0.95], axis=0)

    negative_samples_train, negative_samples_test = np.split(negative_samples, [negative_samples.__len__() * 0.95], axis=0)
    negative_tags_train, negative_tags_test = np.split(negative_tags, [negative_tags.__len__() * 0.95], axis=0)

    train_samples = np.concatenate((positive_samples_train[:], negative_samples_train[:]))
    train_tags = np.concatenate((positive_tags_train[:], negative_tags_train[:]))

    train_samples, train_tags = shuffle_in_unison(train_samples, train_tags)

    return train_samples, train_tags, positive_samples_test, negative_samples_test

def run_nn_solution(input_positive_samples, input_negative_samples):
    train_samples, train_tags, positive_samples_test, negative_samples_test = prepare_data(input_positive_samples, input_negative_samples)

    model = train_model(train_samples, train_tags)

    print 'positive results :'
    print model.predict_proba(positive_samples_test)

    print 'negative results :'
    print model.predict_proba(negative_samples_test)

input_positive_samples = read_file('test.txt')
input_negative_samples = read_file('/temp/negative_keys.txt')

input_positive_samples = input_positive_samples[input_positive_samples[:,0] < 15000]
input_negative_samples = input_negative_samples[input_negative_samples[:,0] < 15000]

input_positive_samples = add_features(input_positive_samples)
input_negative_samples = add_features(input_negative_samples)

fig, ax = plt.subplots()
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
# for name, group in groups:

ax.plot(input_negative_samples[:,0], input_negative_samples[:,2], marker='o', color='r', linestyle='', ms=12, label="negatives")
ax.plot(input_positive_samples[:,0], input_positive_samples[:,2], marker='o', color='g', linestyle='', ms=12, label="positives")

ax.legend()

plt.show()

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