import json
from collections import defaultdict


class seqss_object(object):
    def __init__(self, seq=None):
        """
        seq (string): "AGVLLIKLA"
        """
        self.n = len(seq)
        self.seq = seq

        #It should be a better way to initialize this
        self.probas = []
        d = defaultdict(float)
        d['_'] = 0.
        for s in seq:
            self.probas.append(d.copy())

    def add_probas(self, segment=None, probas=None):
        _probas = probas

        if isinstance(probas,list):
            d = dict()
            for i in xrange(len(probas)):
                d[i] = probas[i]
            _probas = d

        for i in xrange(segment[0], segment[1]):
            for k in _probas:
                self.probas[i][k] += _probas[k]

    def ssassignment(self):
        sseq = ['_'] * self.n
        for i in xrange(self.n):
            key, _ = max(self.probas[i].iteritems(), key=lambda x: x[1])
            sseq[i] = str(key)
        return ''.join(sseq)

    def __repr__(self):
        return json.dumps(self.probas, indent=2)


if __name__ == '__main__':
    seqssobject = seqss_object(seq="AGVLLIKLA")
    seqssobject.add_probas(segment=[2, 5], probas={'a': 0.7, 'b': 0.3})
    seqssobject.add_probas(segment=[1, 6], probas={'a': 0.2, 'b': 0.8})
    seqssobject.add_probas(segment=[3, 6], probas={'l': 1.})
    seqssobject.add_probas(segment=[3, 6], probas=[1.3,0.5])

    print seqssobject.seq
    print seqssobject.ssassignment()
    print seqssobject
