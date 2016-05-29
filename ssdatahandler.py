import seqVectorizer as sv
from sklearn import preprocessing
from keras.utils.np_utils import to_categorical

def create_seq_vectorizer(trainfn='allCATH3_seqVec4_1.txt'):
    seqs = []
    for l in open(trainfn, 'r'):
        l = l.strip().split(',')
        seqs.append(l[3].strip())
    print seqs
    _seqVectorizer = sv.loader(comblength=3, verbose=True)
    #_seqVectorizer.fit_transform(seqs)
    c = ['VFKDGGFTSNDRSVRRYAIRKVLRQMDLGAELGAKTLVLWGGREGAEYDSAKDVSAALDRYREALNL']
    print _seqVectorizer.transform(c)
    return _seqVectorizer


def load_dataset(trainfn='allCATH3_seqVec4_1.txt',min_length=10):
    X, Y = [], []
    for l in open(trainfn, 'r'):
        l = l.strip().split(',')
        _sv = map(float, l[4:])
        if len(_sv) < min_length:continue
        X.append(_sv)
        Y.append(l[2])

    le = preprocessing.LabelEncoder()
    le.fit(Y)
    Y = le.transform(Y)

    return {'X': np.asarray(X),
            'Y': np.asarray(Y),
            'Y_categorical':to_categorical(Y),
            'le':le}
