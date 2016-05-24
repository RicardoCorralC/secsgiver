import random

from sklearn.linear_model import SGDClassifier

import seqVectorizer as sv


def create_seq_vectorizer(trainfn='allCATH3_seqVec4_1.txt'):
    seqs = []
    for l in open(trainfn, 'r'):
        l = l.strip().split(',')
        seqs.append(l[3].strip())
    print seqs
    _seqVectorizer = sv.loader(comblength=3, verbose=True)
    #_seqVectorizer.fit_transform(seqs)
    c = [
        'VFKDGGFTSNDRSVRRYAIRKVLRQMDLGAELGAKTLVLWGGREGAEYDSAKDVSAALDRYREALNL'
    ]
    print _seqVectorizer.transform(c)
    return _seqVectorizer


def load_dataset(trainfn='allCATH3_seqVec4_1.txt'):
    X, Y = [], []
    for l in open(trainfn, 'r'):
        l = l.strip().split(',')
        print l[4:]
        X.append(map(float,l[4:]))
        Y.append(l[2])
    return {'X': np.asarray(X), 'Y': np.asarray(Y)}


if __name__ == '__main__':
    print load_dataset()
