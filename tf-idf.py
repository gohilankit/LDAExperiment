import pandas as pd

#Corpus
docA = "the cat sat on my face"
docB = "the dog sat on my bed"

#Tokenization
bowA = docA.split(" ")
bowB = docB.split(" ")

#All words in all bags
wordSet= set(bowA).union(set(bowB))

#Dictionaries to keep word counts in each document
wordDictA = dict.fromkeys(wordSet, 0)
wordDictB = dict.fromkeys(wordSet, 0)

#Count words in bags
for word in bowA:
    wordDictA[word]+=1

for word in bowB:
    wordDictB[word]+=1

#Create a matrix
pd.DataFrame([wordDictA, wordDictB])

#Compute TF
def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.iteritems():
        tfDict[word] = count / float(bowCount)
    return tfDict

tfBowA = computeTF(wordDictA, bowA)
tfBowB = computeTF(wordDictB, bowB)

#Compute IDF
def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    
    #counts the number of documents that contain a word w
    idfDict = dict.fromkeys(docList[0].keys(),0)
    for doc in docList:
        for word, val in doc.iteritems():
            if val > 0:
                idfDict[word] +=1
                
    #divide N by denominator above, take the log of that
    for word, val in idfDict.iteritems():
        idfDict[word]= math.log(N / float(val)) 

    return idfDict


idfs = computeIDF([wordDictA, wordDictB])

#Compute TF-IDF
def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.iteritems():
        tfidf[word] = val * idfs[word]
    return tfidf

tfidfBowA =  computeTFIDF(tfBowA, idfs)
tfidfBowB = computeTFIDF(tfBowB, idfs)

#Create a weighted matrix
pd.DataFrame([tfidfBowA, tfidfBowB])
