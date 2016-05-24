import itertools
from collections import Counter
import numpy as np
import string
import shelve


SEQVECTORIZERS = shelve.open('SEQvectorizers')


def loader(aaGroupingList='F_Ic4list',comblength=2,scaleFactor=1.5,verbose=False,load_serialize=True):
    object_id = '_'.join(map(str,[aaGroupingList,comblength,scaleFactor]))
    if object_id in SEQVECTORIZERS:
        print 'LOADING'
        return SEQVECTORIZERS[object_id]
    else:
        return seqVectorizer(comblength=comblength,verbose=True)

class seqVectorizer(object):

    def __init__(self,aaGroupingList='F_Ic4list',comblength=5,scaleFactor=1.5,verbose=False,load_serialize=True):
        """
        Arguments initializes variables used by various functions, nevertheles,
        each member function can be called statical if needed with another arguments.

        Keyword arguments:
        normalAAslist -- Each element is a string with aminoacids to be considered as equivalent.
                            Ordering is not important.
                            If a string, it is considered as a key for internal aaLmapsDict.
        comblength    -- The maximum size of combinations to be considered.
        """

        self.object_id = '_'.join(map(str,[aaGroupingList,comblength,scaleFactor]))

        #WARNING X aminoacid introduced
        self.aaLmapsDict = {'normalAAslist' : ['A','R','N','D','C','E','Q','G','H','I','L','K','M','F','P','S','T','W','Y','V','X'],
                            'F_Ic4list' : ['AWM','GST','HPY','CVIFL','DNQ','ER','K','X'],
                            'MSlist' : ['AVLIMC','WYHF','TQSN','RK','ED','GP','X'],
                            'LESKlist' : ['AST', 'CVILWYMPF','HQN','RK','ED','G','X']}
        if type(aaGroupingList) == str:
            self.aaGroupingList = self.aaLmapsDict[aaGroupingList]
        else:
            self.aaGroupingList = aaGroupingList  #Assuming aaGroupingList is already a list mapping

        self.comblength = comblength
        self.maxElements = []  #The maximum number observed in each component. It is used to normalize final vector.
        self.scaleFactor = scaleFactor  #Factor scaling each of the self.maxElements values for normalizing
        self.epsilon = 0.0001
        self.numAttributes = 0
        self.verbose = verbose



    def dictFromListMapping(self,L):
        """
        Creates a dictionary containing the mapping depicted in list L
        """
        D = dict()
        for i in xrange(len(L)):
            for a in L[i]:
                D[a] = string.ascii_letters[i]
        return D



    def mapSeq(self,S,M):
        """
        Returns the transformed string S given the mapping in dictionary M
        """
        res = ''.join([M[c] for c in S])
        return res


    def getFreqsDict(self,seq,dictmap,n):
        """
        returns a list with frequences of combinations from 2 to n of aminoacids in seq with residue mapping dictmap
        """
        combsCounter = Counter()
        for i in xrange(2,n+1):
            for j in xrange(len(seq)-i):
                strKey = ''.join(sorted(self.mapSeq(seq[j:j+i],dictmap)))
                combsCounter[strKey] += 1

        return combsCounter

    def iterAACombs(self,n,alfabet):
        """
        returns a list with all combinations of aminoacids from length 2 to n
        """
        AAs = alfabet
        AAcombsList = []
        for i in xrange(2,n+1):
            for combs in itertools.combinations_with_replacement(AAs,i): #itertools.product(AAs, repeat=i):
                yield ''.join(sorted(combs))


    def createAAFreqVector(self,seq,L,n,normalize=False):
        """
        returns an array with frequecies of each aa combination
        """
        d = self.dictFromListMapping(L)
        AAfreqsList = []
        C = self.getFreqsDict(seq,d,n)
        alfab = ''.join([string.ascii_letters[i] for i in xrange(len(L))])
        for i in self.iterAACombs(n,alfab):
            AAfreqsList.append(C[i])
        if normalize: return  (AAfreqsList - np.min(AAfreqsList, 0)) / (np.max(AAfreqsList, 0) + 0.0001) #Deprecated
        return AAfreqsList

    def fit_transform(self,seqs):
        X = map(lambda s : np.array(self.createAAFreqVector(s,self.aaGroupingList,self.comblength)) , seqs)
        X = np.asarray(X, dtype=np.float)
        if self.verbose: print X
        a,self.numAttributes = X.shape
        self.maxElements = []
        for i in xrange(self.numAttributes):
            tmpf = np.max(X[:,i])
            self.maxElements.append(tmpf)
            f = float(tmpf*self.scaleFactor+self.epsilon)
            X[:,i] = np.multiply(X[:,i],(1/f))

        #Object persistence
        SEQVECTORIZERS[self.object_id] = self

        return X

    def transform(self,seqs):
        """
        Transform raw sequences into attribute vectors
        fit_transform must be called first
        """
        X = map(lambda s : np.array(self.createAAFreqVector(s,self.aaGroupingList,self.comblength)) , seqs)
        X = np.asarray(X, dtype=np.float)
        if self.verbose: print X
        for i in xrange(self.numAttributes):
            f = float(self.maxElements[i]*self.scaleFactor+self.epsilon)
            X[:,i] = np.multiply(X[:,i],(1/f))
        return X

def main():

    #_seqVectorizer = seqVectorizer(comblength=2,verbose=True)
    _seqVectorizer = loader(comblength=3,verbose=True)
    a = ['MGQPGNGSAFLLAPNGSHAPDHDVTQERDEVWVVGMGIVMSLIVLAIVFGNVLVITAIAKHVQNLSQVEQDGRTGHGLRRSSKFCLKEHKALKTLGIIMGTFTLCWLPFFIVNIVHVIQD',
         'GEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRFKHLKTEAEMKASEDLKKAGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQ']
    print _seqVectorizer.fit_transform(a)
    c = ['VFKDGGFTSNDRSVRRYAIRKVLRQMDLGAELGAKTLVLWGGREGAEYDSAKDVSAALDRYREALNLLAQYSEDRGYGLRFAIEPKPNQPRGDILLPTAGHAIAFVQELERPELFGINPETGHEQMSNL']
    print _seqVectorizer.transform(c)

if __name__== '__main__':
    main()
