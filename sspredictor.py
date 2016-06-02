import random
import shelve

import numpy as np
from keras.layers import Activation, Dense, Dropout, Input
from keras.models import Model, Sequential
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC

import seqVectorizer as sv
import ssdatahandler


class nnclf(object):
    def __init__(self,
                 input_dim=None,
                 output_dim=None,
                 num_layers=2,
                 num_neurons_by_layer=100,
                 init='lecun_uniform',
                 activation='relu'):

        self.input_dim = input_dim
        self.model = Sequential()

        #first layer
        self.model.add(Dense(num_neurons_by_layer,
                             input_dim=input_dim,
                             init=init))
        self.model.add(Activation(activation))
        self.model.add(Dropout(0.3))

        #hidden layers
        for nl in xrange(num_layers - 1):
            self.model.add(Dense(num_neurons_by_layer,
                                 input_dim=num_neurons_by_layer,
                                 init=init))
            self.model.add(Activation(activation))
            self.model.add(Dropout(0.3))

        #output layer
        self.model.add(Dense(output_dim,
                             input_dim=num_neurons_by_layer,
                             init=init))
        self.model.add(Activation('softmax'))

        self.model.compile(optimizer='adagrad',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])

    def fit(self, X, Y):
        self.model.fit(X, Y, nb_epoch=10, batch_size=32)

    def predict(self, X):
        self.model.predict(X)

    def score(X_test, y_test):
        score = model.evaluate(X_test, y_test, batch_size=16)
        return score

    def get_params(self, deep=True):
        return {"input_dim": self.input_dim}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            self.setattr(parameter, value)
        return self


def main():
    print '*** loading dataset...'
    dataset = ssdatahandler.load_dataset()
    print '*** dataset loaded'

    clf = nnclf(input_dim=len(dataset['X'][0]),
                output_dim=len(dataset['Y_categorical'][0]))

    X_train, X_test, y_train, y_test = train_test_split(
        dataset['X'],
        dataset['Y_categorical'],
        test_size=0.3)

    print '\n*** Starting training'
    clf.fit(X_train, y_train)
    print '***Training finished\n'

    score = clf.score(X_test, y_test)

    print 'nnclf', score

    clf = SGDClassifier()
    scores = cross_validation.cross_val_score(clf,
                                              dataset['X'],
                                              dataset['Y'],
                                              cv=5)
    print 'SGD', scores

    #D = she
    #if not 'clf' in


if __name__ == '__main__':
    print main()
