import _thread
import codecs
import glob
import logging
import os
import zipfile
from os.path import expanduser

import networkx as nx
import nltk
import numpy as np
import pandas as pd
import wget as wget
from PyQt5.QtWidgets import QDialogButtonBox, QFileDialog
from sklearn.metrics.pairwise import cosine_similarity

from Utils.DialogBuilder import DialogBuilder

"""
This logic here is taken from https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
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
        logging.info("Created instance of summarizer class")
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
        logging.info("Starting to generate summary")

        from nltk.tokenize import sent_tokenize

        # break text into sentences
        sentences = sent_tokenize(text)

        # do nothing if there are not words passed
        if not sentences:
            logging.warning("Document has no text")
            return ""

        # clean the data of unnecessary values
        clean_sentences = self.cleanSentences(sentences)

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
        logging.info("Finished generating summary")
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
        logging.info("Downloading nltk stopwords")
        nltk.download('stopwords')

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        logging.info("Downloading nltk punkt")
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


#################################################################
# HANDLING DOWNLOADS

def onSummaryAction(app, document):
    """
    This spawns the prompt for the user to get the word embeddings needed for the doc summarizer
    :param app: Reference to the application
    :param document: Reference to the document
    :return: Returns nothing
    """

    # The action that gets called when the user selects a button on the prompt
    def onDialogButtonClicked(button):
        dependencyDialogHandler(app, button, document)

    # if summarizer has not been created create it
    if app.summarizer is None:
        logging.info("Doc Summarizer not initialized. Prompting user for dependency download")
        # prompt the user to select or Download the word word_embeddings
        download_dialog = DialogBuilder(app, "Dictionaries",
                                        "Would you like to download required dictionaries?",
                                        "If you have already downloaded them previously click open to select the location on disk.")
        buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Open | QDialogButtonBox.Yes)
        download_dialog.addButtonBox(buttonBox)
        buttonBox.clicked.connect(onDialogButtonClicked)
        download_dialog.exec()
    # if there is already an instance of the summarizer
    else:
        logging.info(app.summarizer.summarize(document.toPlainText()))


def dependencyDialogHandler(app, button, document=None):
    """
    This will handle the users choice for the Download prompt the user will select where they want to find/Download the files
    :param app: an application reference
    :param button: the button the user selected
    :return:
    """
    logging.info("User selected " + button.text())
    if button.text() == 'Cancel':
        return

    path_existing = QFileDialog.getExistingDirectory(app, "Select Folder To Download To",
                                                     expanduser("~"),
                                                     QFileDialog.ShowDirsOnly
                                                     | QFileDialog.DontResolveSymlinks)
    if path_existing == "":
        logging.info("User Cancelled File Dialog")
        return

    path_new = os.path.join(path_existing, 'WordEmbeddings')



    def files_exist(path1: str, path2: str):
        if os.path.exists(os.path.join(path1, 'glove.6B.100d.vocab')) and os.path.exists(
                os.path.join(path1, 'glove.6B.100d.npy')):
            return path1
        elif os.path.exists(os.path.join(path2, 'glove.6B.100d.vocab')) and os.path.exists(
                os.path.join(path2, 'glove.6B.100d.npy')):
            return path2
        else:
            return None

    existing_path = files_exist(path_existing, path_new)
    if existing_path == None:
        zip_file = 'glove.6B.100d.zip'

        if not os.path.exists(os.path.join(path_new, zip_file)):
            logging.info("Missing Files and ZIP. To re-download")
            if button.text() == "Open":
                logging.info("Dictionaries not found in directory. Prompting user for download")
                download_dialog = DialogBuilder(app, "Error!",
                                                "Error - Dictionaries not found!",
                                                "Please select a different path or download them again.")
                button_box = QDialogButtonBox(QDialogButtonBox.Ok)
                download_dialog.addButtonBox(button_box)
                download_dialog.exec()
                return
            if not ensureDirectory(app, path_new):
                return
            should_download = True
        else:
            logging.info("Found ZIP: " + zip_file + ". No need for re-download")
            should_download = False

        try:
            _thread.start_new_thread(getWordEmbeddings, (app, path_new, should_download, document))
        except:
            logging.error("Unable to start thread")
    else:
        logging.info("Found glove.6B.100d.vocab and glove.6B.100d.npy")
        # fill the dictionary with the word embeddings
        model = fillModel(existing_path)
        # create an instance of the summarizer and give it to the application
        app.summarizer = Summarizer(model)
        if document is not None:
            app.summarizer.summarize(document.toPlainText())


def ensureDirectory(app, path):
    if not os.path.exists(path):
        logging.info("Creating WordEmbeddings directory")
        try:
            os.mkdir(path)
            return True
        except:
            return False
    else:
        logging.info("Download path directory already exists")
        clear_dialog = DialogBuilder(app, "Download directory WordEmbeddings already exists...",
                                     "Would you like to clear the contents and proceed?",
                                     "Cancel will stop the download.")
        buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
        clear_dialog.addButtonBox(buttonBox)

        if clear_dialog.exec():
            logging.info("User chose to remove all contents")
            files = glob.glob(os.path.join(path, '*'))
            for f in files:
                try:
                    os.remove(f)
                except:
                    dialog_fail = DialogBuilder(app, "Removing contents failed\nPermission denied")
                    dialog_fail.show()
                    return False
            return True
        else:
            logging.info("User chose not to clear directory. Exiting download")
            return False


def getWordEmbeddings(app, path: str, should_download=True, document=None):
    """
    This will download the necessary files for Summarizer then create the word embedding model and create
    an instance of the summarizer
    :param app: A reference to the application
    :param path: A path to where the files are or are to be downloaded
    :param should_download: Whether or not to re-download zip
    :param document: Optionally summarize text at the end of procedure
    :return:
    """
    zip_file = 'glove.6B.100d.zip'
    if should_download:
        # Download the actual files
        logging.info("Started Downloading")
        # Download the word embeddings file from http://hunterprice.org/files/glove.6B.100d.zip
        # this file is taken from stanfords pre trained glove word embeddings https://nlp.stanford.edu/projects/glove/
        url = "http://hunterprice.org/files/" + zip_file
        wget.download(url, out=path)
        logging.info("Finished downloading")

    # uncompress the files
    logging.info("Started unzipping")
    with zipfile.ZipFile(os.path.join(path, zip_file), 'r') as zip_ref:
        zip_ref.extractall(path)
    logging.info("Finished unzipping")

    try:  # delete the compressed file
        os.remove(os.path.join(path, zip_file))
        logging.info("Deleted zip file")
    except:
        logging.warning("Error while removing leftover ZIP file")

    # fill the dictionary with the word embeddings
    model = fillModel(path)
    # create an instance of the summarizer and give it to the application
    app.summarizer = Summarizer(model)
    # if text was passed in then also perform summary
    if document is not None:
        app.summarizer.summarize(document.toPlainText())


def fillModel(path):
    """
    takes the path to the word embedding files and fills a dictionary with the (word: word vector) pairs
    :param path: path to the word embedding files
    :return: Returns a dictionary of word vectors
    """
    path = os.path.join(path, "glove.6B.100d")
    path_vocab = path + '.vocab'
    path_npy = path + '.npy'

    # check to make sure the glove files exist
    if not os.path.exists(path_vocab):
        logging.error('Path does not exist - ' + path_vocab)
        return

    # check to make sure the glove files exist
    if not os.path.exists(path_npy):
        logging.error('Path does not exist - ' + path_npy)
        return

    # read the files into a python dict
    logging.info("Attempting to read dictionary contents")
    with codecs.open(path_vocab, 'r', 'utf-8') as f_in:
        index2word = [line.strip() for line in f_in]
    wv = np.load(path_npy)
    model = {}
    for i, w in enumerate(index2word):
        model[w] = wv[i]
    logging.info("Finished reading dictionary contents")
    return model
