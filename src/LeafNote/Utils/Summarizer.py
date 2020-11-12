"""
this module holds a class to summarize any given class
"""

import codecs
import glob
import logging
import os
import zipfile

import networkx as nx
import nltk
import numpy as np
import pandas as pd
import wget
from PyQt5.QtWidgets import QDialogButtonBox, QFileDialog
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity

from LeafNote.Utils import DialogBuilder
from LeafNote.Utils.ThreadBuilder import ExecuteThread


class Summarizer:
    """
    This class will compute a summary of any given text
    """

    def __init__(self, word_embeddings):
        """
        This logic here is taken from
        https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
        The word embeddings are taken from standford pre trained glove word embeddings
        https://nlp.stanford.edu/projects/glove/
        In this file you will find the implementation of the text rank algorithm. The goals is to
        take in an article or any amount of text and develop a summary of the text.
        The algorithm is split into 5 steps:
            1. Split the text into sentences
            3. Find the vector representation (word embeddings) for every sentence
            4. Calculate the similarities between the sentence vectors and store
                them into a similarity matrix.
            5. A certain number of top-ranked sentences form the final summary
        """
        logging.debug("Creating Document Summarizer")

        handlePackageDownloads()
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
        :return: Returns a string of the summary
        """
        logging.info("Starting to generate summary")

        # break text into sentences
        sentences = sent_tokenize(text)

        # do nothing if there are not words passed
        if not sentences:
            logging.warning("Document has no text")
            return "No summary available"

        # clean the data of unnecessary values
        clean_sentences = self.cleanSentences(sentences)

        # create vectors for each of our sentences
        self.sentence_vectors = []
        self.createSentenceVectors(clean_sentences)

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
        logging.debug("")
        clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

        # make alphabets lowercase
        clean_sentences = [s.lower() for s in clean_sentences]

        # eliminate all stop words from the sentences
        clean_sentences = [removeStopwords(sent.split(), self.stopwords) for sent in
                           clean_sentences]
        return clean_sentences

    def createSentenceVectors(self, clean_sentences):
        """
        this will creates a list of sentence vectors from the given clean sentences
        :param clean_sentences: a list of sentences without stopwords
        :return: Returns nothing
        """
        # for each sentence we fetch vectors for their respective words
        # then we take the mean of those vectors to get a consolidated vector for the sentence
        logging.debug("")
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
        logging.debug("")
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


def handlePackageDownloads():
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


def removeStopwords(sen, stop_words):
    """
    this will remove all stopwords from a given sentence and return the new cleaned sentence
    the sentence must be a list of words: ["this", "is", "a", "sentence"]
    :param sen: the sentence to be cleaned
    :param stop_words: the list of stopwords to remove
    :return: Returns the cleaned sentence
    """
    new_sent = " ".join([i for i in sen if i not in stop_words])
    return new_sent


#################################################################
# HANDLING DOWNLOADS

def onSummaryAction(app, document):
    """
    This spawns the prompt for the user to get the word embeddings needed for the doc summarizer
    :param app: Reference to the application
    :param document: Reference to the document
    :return: Returns summarized text if dictionaries are found
    """

    # The action that gets called when the user selects a button on the prompt
    def onDialogButtonClicked(button):
        """
        Handler for button click in dialog
        """
        dependencyDialogHandler(app, button, document)

    # if summarizer has not been created create it
    if document.summarizer is None:
        logging.info("Summarizer NOT initialized. Prompting user for dependency download.")
        # prompt the user to select or Download the word word_embeddings
        download_dialog = DialogBuilder(app, "Dictionaries",
                                        "Would you like to download required dictionaries?",
                                        "If you have already downloaded them previously "
                                        "click open to select the location on disk.")
        button_box = QDialogButtonBox(
            QDialogButtonBox.Cancel | QDialogButtonBox.Open | QDialogButtonBox.Yes)
        download_dialog.addButtonBox(button_box)
        button_box.clicked.connect(onDialogButtonClicked)
        download_dialog.exec()
        return None

    # if there is already an instance of the summarizer
    logging.info("Summarizer is already initialized!")
    return document.summarizer.summarize(document.toPlainText())


def ensureDirectory(app, path: str):
    """
    This will ensure that the directory we are saving the embedding files into exists.
    :param app: reference to the application
    :param path: path to the directory
    :return: Returns true on success and false otherwise
    """
    # if the path doesnt exist make the directory
    if not os.path.exists(path):
        try:
            os.mkdir(path)
            logging.info("Created WordEmbeddings directory")
            return True
        except OSError as e:
            logging.exception(e)
            logging.error("Failed to create directory")
            return False
    # if it does exist prompt the user to clear the directory
    else:
        logging.info("Download path directory already exists!")

        # create the dialog to warn the user the dir will be cleared
        clear_dialog = DialogBuilder(app, "Download directory WordEmbeddings already exists...",
                                     "Would you like to clear the contents and proceed?",
                                     "Cancel will stop the download.")
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Yes)
        clear_dialog.addButtonBox(button_box)

        # clear the directory if selected by the user
        if clear_dialog.exec():
            logging.info("User chose to remove all contents")
            files = glob.glob(os.path.abspath(os.path.join(path, '*')))
            for f in files:
                try:
                    os.remove(f)
                    logging.debug("Removed: %s", f)
                except OSError as e:
                    dialog_fail = DialogBuilder(app, "Removing contents failed\nPermission denied")
                    dialog_fail.show()
                    logging.exception(e)
                    logging.error("Error occured removing directory contents")
                    return False
            return True

        logging.info("User chose not to clear directory. Exiting download")
        return False


def dependencyDialogHandler(app, button, document=None):
    """
    This will handle the users choice for the Download prompt the user will select where they
    want to find/Download the files
    :param app: an application reference
    :param button: the button the user selected
    :param document: document reference
    :return: returns summary
    """
    logging.debug("User selected %s", button.text())

    # quit if the user selected cancel
    if button.text() == '&Cancel':
        return

    path_parent = QFileDialog.getExistingDirectory(app, "Select Folder To Download To",
                                                   app.left_menu.model.rootPath(),
                                                   QFileDialog.ShowDirsOnly
                                                   | QFileDialog.DontResolveSymlinks)
    if path_parent == "":
        logging.info("User Cancelled File Dialog")
        return

    path_child = os.path.abspath(os.path.join(path_parent, 'WordEmbeddings'))

    def files_exist(path1: str, path2: str):
        """
        Checks if the files exist within any of the 2 directories
        """
        if os.path.exists(
                os.path.abspath(os.path.join(path1, 'glove.6B.100d.vocab'))) and\
                os.path.exists(os.path.abspath(os.path.join(path1, 'glove.6B.100d.npy'))):
            return path1
        if os.path.exists(
                os.path.abspath(os.path.join(path2, 'glove.6B.100d.vocab'))) and \
                os.path.exists(os.path.abspath(os.path.join(path2, 'glove.6B.100d.npy'))):
            return path2
        return None

    existing_path = files_exist(path_parent, path_child)

    if existing_path is None:
        zip_file = 'glove.6B.100d.zip'

        # prompt the user that they need to download the dependency files
        if not os.path.exists(os.path.abspath(os.path.join(path_child, zip_file))):
            logging.warning("Missing Files and ZIP. To re-download")
            if button.text() == "Open":
                logging.error("Dictionaries not found in directory")
                download_dialog = DialogBuilder(app, "Error!",
                                                "Error - Dictionaries not found!",
                                                "Please select a different path"
                                                " or download them again.")
                button_box = QDialogButtonBox(QDialogButtonBox.Ok)
                download_dialog.addButtonBox(button_box)
                download_dialog.exec()
                return
            if not ensureDirectory(app, path_child):
                return
            should_download = True
            # create loading bar dialog and start the download thread
            progress_bar_dialog = DialogBuilder(app, "Download Progress",
                                                "Downloading Dictionaries...",
                                                "Please do not close this window")
            progress_bar = progress_bar_dialog.addProgressBar((0, 100))
            progress_bar_dialog.open()
        else:
            logging.info("Found ZIP: %s. No need for re-download", zip_file)
            should_download = False
            progress_bar = None

        if app.thread_placeholder is None:
            app.thread_placeholder = ExecuteThread(getWordEmbeddings,
                                                   (path_child, should_download, progress_bar))

            def callback():
                """
                Callback for our thread
                """
                result = app.thread_placeholder.getReturn()
                if result is True:
                    logging.debug("Summarizer Thread Finished")
                    initializeSummarizer(path_child, app, document)
                    app.thread_placeholder = None
                    app.right_menu.updateSummary()
                else:
                    logging.error("Thread finished unsuccessfully")

            app.thread_placeholder.setCallback(callback)
            app.thread_placeholder.start()
        else:
            logging.warning("Thread placeholder already in use")
    else:
        logging.info("Found glove.6B.100d.vocab and glove.6B.100d.npy")

        # fill the dictionary with the word embeddings
        initializeSummarizer(existing_path, app, document, True)


def getWordEmbeddings(path: str, should_download: bool = True,
                      progress_bar=None):
    """
    This will download the necessary files for Summarizer
    then create the word embedding model and create
    an instance of the summarizer
    :param path: A path to where the files are or are to be downloaded
    :param should_download: Whether or not to re-download zip
    :param progress_bar: A reference to the progress bar
    :return:
    """
    zip_file = 'glove.6B.100d.zip'
    if should_download:
        # open the progress dialogue
        logging.info("Started Downloading Word Embeddings")
        if progress_bar is None:
            logging.error("Progress bar is None")
            return False

        # function to update the progress bar
        def progressBarSignal(current, total, width):
            """
            Change the progress bar
            """
            logging.debug("Progress: %s out of %s ... width %s", current, total, width)
            progress_bar.setMaximum(total)
            progress_bar.setValue(current)

        # Download the word embeddings file from http://hunterprice.org/files/glove.6B.100d.zip
        # this file is taken from stanfords pre trained glove
        # word embeddings https://nlp.stanford.edu/projects/glove/
        url = "http://hunterprice.org/files/" + zip_file
        wget.download(url, out=path, bar=progressBarSignal)
        logging.info("Finished downloading!")

    # uncompress the files
    logging.info("Started unzipping")
    with zipfile.ZipFile(os.path.abspath(os.path.join(path, zip_file))) as zip_ref:
        zip_ref.extractall(path)
    logging.info("Finished unzipping")

    try:  # delete the compressed file
        os.remove(os.path.abspath(os.path.join(path, zip_file)))
        logging.info("Deleted zip file")
    except OSError as e:
        logging.exception(e)
        logging.warning("Failed to remove leftover ZIP file")
        return False

    return True


def initializeSummarizer(path, app, document, update_right_menu=False):
    """
    Initializes a summarizer instance
    """
    model = createModel(path)
    if model is not None:
        # create an instance of the summarizer and give it to the application
        app.settings.setValue("dictionaryPath", path)
        if document is not None:
            document.summarizer = Summarizer(model)
            if update_right_menu:
                app.right_menu.updateSummary()
        else:
            logging.warning("Document is None - Not initializing Summarizer!")
    else:
        logging.error("Model ERROR - Failed to initialize Summarizer!")


def createModel(path):
    """
    takes the path to the word embedding files and fills
     a dictionary with the (word: word vector) pairs
    :param path: path to the word embedding files
    :return: Returns a dictionary of word vectors
    """
    logging.debug("Start fill model - reading dictionaries")
    path = os.path.abspath(os.path.join(path, "glove.6B.100d"))
    path_vocab = path + '.vocab'
    path_npy = path + '.npy'

    # check to make sure the glove files exist
    if not os.path.exists(path_vocab):
        logging.error('Path does not exist - %s', path_vocab)
        return None

    # check to make sure the glove files exist
    if not os.path.exists(path_npy):
        logging.error('Path does not exist - %s', path_npy)
        return None

    # read the files into a python dict
    logging.debug("Attempting to read dictionary contents")
    with codecs.open(path_vocab, encoding='utf-8') as f_in:
        index2word = [line.strip() for line in f_in]
    wv = np.load(path_npy)
    model = {}
    for i, w in enumerate(index2word):
        model[w] = wv[i]
    logging.debug("Finished reading dictionary contents")
    return model
