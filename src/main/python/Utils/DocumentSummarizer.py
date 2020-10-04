import codecs
import os
import logging
import numpy as np
import pandas as pd
import nltk
import wget as wget
from PyQt5.QtCore import QRunnable
from PyQt5.QtWidgets import QDialogButtonBox
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import zipfile

from Utils.DialogBuilder import DialogBuilder

"""
This logic here is taken from https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/\
The word embeddings are taken from standford pre trained glove word embeddings https://nlp.stanford.edu/projects/glove/
In this file you will find the implementation of the text rank algorithm. The goals is to
take in an article or any amount of text and develop a summary of the text.
The algorithm is split into 5 steps:
    1. Split the text into sentences
    3. Find the vector representation (word embeddings) for every sentence
    4. Calculate the similarities between the sentence vectors and store
        them into a similarity matrix.
    5. A certain number of top-ranked sentences form the final summary
"""


class Summarizer:
    def __init__(self, word_embeddings):
        """
        Sets up class variables.
        """
        handleDownloads()
        from nltk.corpus import stopwords
        self.word_embeddings = word_embeddings
        self.sentence_vectors = []
        self.sim_mat = []
        self.ranked_sentences = []
        self.summary = ""

        # get a list of english stop words
        # stopwords are commonly used words of a language (we want to get rid of these words)
        self.stopwords = stopwords.words('english')

    def summarize(self, text: str, summary_size: int = 5):
        """
        This will take in text and the size of a summary and generate a summary of the text.
        :param text: text from a document.
        :param summary_size: the number of sentences in the summary
        """
        handleDownloads()
        from nltk.tokenize import sent_tokenize

        # break text into sentences
        sentences = sent_tokenize(text)

        # clean the data of unnecessary values
        clean_sentences = self.cleanSentences(sentences)

        # Extract word vectors and create a dictionary with key value pairs 'word', [word vector]
        # https://nlp.stanford.edu/projects/glove/ for the precalculated word vectors
        # self.word_embeddings = {}
        # f = open('glove.6B.100d.txt', encoding='utf-8')
        # for line in f:
        #     values = line.split()
        #     word = values[0]
        #     coefs = np.asarray(values[1:], dtype='float32')
        #     self.word_embeddings[word] = coefs
        # f.close()

        # create vectors for each of our sentences
        self.sentence_vectors = []
        self.createWordVectors(clean_sentences)

        # create a similarity matrix of the sentences
        self.sim_mat = np.zeros([len(sentences), len(sentences)])
        self.createSimilarityMatrix(len(sentences))

        # create a directed graph from the similarity matrix
        # then generate rankings for the sentences
        nx_graph = nx.from_numpy_array(self.sim_mat)
        scores = nx.pagerank(nx_graph)

        # extract top n sentences as the summary
        self.ranked_sentences = sorted(((scores[i], s)
                                        for i, s in enumerate(sentences)), reverse=True)
        # self.ranked_sentences = self.ranked_sentences[:]
        self.ranked_sentences = [s[1] for s in self.ranked_sentences]
        self.summary = sentToText(self.ranked_sentences[:summary_size])
        return self.summary

    def cleanSentences(self, sentences):
        """
        this takes a list of sentences and returns the cleaned sentences for the alg.
        :param sentences: a list of sentences that need to be cleaned
        :return: returns the cleaned sentences
        """
        # use regex expression to eliminate all non letter characters
        clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

        # make alphabets lowercase
        clean_sentences = [s.lower() for s in clean_sentences]

        # eliminate all stop words from the sentences
        clean_sentences = [removeStopwords(sent.split(), self.stopwords) for sent in clean_sentences]
        return clean_sentences

    def createWordVectors(self, clean_sentences):
        """
        this will creates a list of sentence vectors from the given clean sentences
        :param clean_sentences: a list of sentences without stopwords
        :return: Returns nothing
        """
        # for each sentence we fetch vectors for their respective words
        # then we take the mean of those vectors to get a consolidated vector for the sentence
        for i in clean_sentences:
            if len(i) != 0:
                v = sum([self.word_embeddings.get(w, np.zeros((100,)))
                         for w in i.split()]) / (len(i.split()) + 0.001)
            else:
                v = np.zeros((100,))
            self.sentence_vectors.append(v)

    def createSimilarityMatrix(self, n):
        """
        this will create a similarity matrix of all of the sentences
        the nodes of the matrix represent the sentences
        the edges represent the similarity between the two sentences
        :param n: the size of the square matrix
        :return: Returns nothing
        """
        # for each index in the matrix calculate the cosine similarity
        # for more information on cosine similarity: https://en.wikipedia.org/wiki/Cosine_similarity
        for i in range(n):
            for j in range(n):
                if i != j:
                    self.sim_mat[i][j] = \
                        cosine_similarity(self.sentence_vectors[i].reshape(1, 100),
                                          self.sentence_vectors[j].reshape(1, 100))[0, 0]


#################################################################
# HELPER FUNCTIONS

def sentToText(text, separator=' '):
    """
    converts a list of sentences into one string separated by a user value
    :param text: a list of sentences
    :param separator: the separator between the sentences
    :return: returns a string holding the concatenated sentences.
    """
    sentence = ""
    for s in text:
        sentence += str(s) + str(separator)
    return sentence


def handleDownloads():
    """
    this downloads the nltk packages in the nltk module needed for this file
    :return: Returns nothing
    """
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading nltk stopwords")
        nltk.download('stopwords')

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading nltk punkt")
        nltk.download('punkt')


def removeStopwords(sen, stopwords):
    """
    this will remove all stopwords from a given sentence and return the new cleaned sentence
    the sentence must be a list of words: ["this", "is", "a", "sentence"]
    :param sen: the sentence to be cleaned
    :param stopwords: the list of stopwords to remove
    :return: Returns the cleaned sentence
    """
    new_sent = " ".join([i for i in sen if i not in stopwords])
    return new_sent


def getWordEmbeddings(path, app, download=True):

    # if cannot find both of the wv files
    if not os.path.exists(path+'glove.6B.100d.vocab') and not os.path.exists(path+'glove.6B.100d.npy'):
        # if cannot find the .zip file
        if not os.path.exists(path + 'glove.6B.100d.zip'):
            if not download:
                download_dialog = DialogBuilder(app, "Could not Find Word Vectors",
                                                "Would you like to download the dependencies?",
                                                "The directory you selected does not contain the necessary files.")
                buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
                download_dialog.addButtonBox(buttonBox)
                if not download_dialog.exec():
                    return
            # create the directory to hold  the word embeddings
            path = os.path.join(path, 'WordEmbeddings/')
            print('########',path)
            os.mkdir(path)

            # download the word embeddings file from http://hunterprice.org/files/glove.6B.100d.zip
            # this file is taken from stanfords pre trained glove word embeddings https://nlp.stanford.edu/projects/glove/
            url = "http://hunterprice.org/files/glove.6B.100d.zip"
            wget.download(url, out=path)

        # create a directory for the files
        # uncompress the files
        with zipfile.ZipFile(path+'glove.6B.100d.zip', 'r') as zip_ref:
            zip_ref.extractall(path)

        # delete the compressed file
        os.remove(path+'glove.6B.100d.zip')

    logging.info("Downloaded Word Embeddings")
    path = path + "glove.6B.100d"

    # check to make sure the glove files exist
    if not os.path.exists(path + '.vocab'):
        logging.error('Path does not exist - '+path+'.vocab')
        return

    # check to make sure the glove files exist
    if not os.path.exists(path + '.npy'):
        logging.error('Path does not exist - ' + path + '.npy')
        return

    # read the files into a python dict
    with codecs.open(path + '.vocab', 'r', 'utf-8') as f_in:
        index2word = [line.strip() for line in f_in]
    wv = np.load(path + '.npy')
    model = {}
    for i, w in enumerate(index2word):
        model[w] = wv[i]

    app.summarizer = Summarizer(model)

