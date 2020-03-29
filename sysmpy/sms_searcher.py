from gensim import corpora
from gensim import similarities
from gensim import models
from collections import defaultdict
import re
import os
import nbformat
import os.path
import warnings

class SMS2Texts():
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.texts = []

        isdir = os.path.isdir(base_dir)
        if isdir is False:
            warnings.simplefilter(f'The directory {base_dir} does not exist!')

    def take_only_quotation_mark(self, data):
        quotes = re.findall(r'"[^"]*"', data, re.U)
        quotes = " ".join(quotes)
        quotes = quotes.replace('"', '')
        return quotes

    def take_only_source_from_ipynb(self, data):
        quotes = re.findall(r'"[^"]*"', data, re.U)
        quotes = " ".join(quotes)
        quotes = quotes.replace('"', '')
        return quotes

    def collect_files(self):
        """
        This collects all files and performs indexing
        """
        self.texts.clear()

        for f_name in os.listdir(self.base_dir):
            text_info = {}
            if f_name.endswith(".py"):
                source_path = os.path.join(self.base_dir, f_name)
                text_info['file'] = source_path
                with open(source_path) as f:
                    data = f.read()
                    source = self.take_only_quotation_mark(data)
                    text_info['text'] = source
                    self.texts.append(text_info)
            elif f_name.endswith(".ipynb"):
                source_path = os.path.join(self.base_dir, f_name)
                text_info['file'] = source_path
                with open(source_path) as f:
                    notebook = nbformat.read(f, as_version=nbformat.NO_CONVERT)
                    source = ''
                    for cell in notebook.cells:
                        data = cell['source']
                        source += self.take_only_source_from_ipynb(data)
                    text_info['text'] = source
                    self.texts.append(text_info)


class SMSSearcher():
    def __init__(self, path):
        u2t = SMS2Texts(path)
        u2t.collect_files()
        # print(u2t.texts)
        self.texts = u2t.texts

        # Create a set of frequent words
        stoplist = set('for a of the and to in'.split(' '))

        # Remove special symbols
        text_corpus = []
        for text in self.texts:
            text_corpus.append(text['text'])

        text_corpus_cleaned = [re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", file) for file in text_corpus]

        # Lowercase each document, split it by white space and filter out stopwords
        texts = [[word for word in document.lower().split() if word not in stoplist] for document in text_corpus_cleaned]

        # Count word frequencies
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        # Only keep words that appear more than once
        # processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
        # Only keep words that appear more than once
        processed_corpus = [[token for token in text if frequency[token] > 0] for text in texts]

        # This dictionary defines the vocabulary of all words that our processing knows about.
        self.dictionary = corpora.Dictionary(processed_corpus)
        # for k, v in self.dictionary.items():
        #     print(f'{k} = [{v}]')

        # We can convert our entire original corpus to a list of vectors:
        bow_corpus = [self.dictionary.doc2bow(text) for text in processed_corpus]

        # train the model
        self.tfidf = models.TfidfModel(bow_corpus)

        self.index = similarities.SparseMatrixSimilarity(self.tfidf[bow_corpus], num_features=len(self.dictionary))
        # self.index = similarities.SparseMatrixSimilarity(self.tfidf[bow_corpus], num_features=400)
        # print(self.index)

    def search(self, query_words):
        ###############################################################################
        # and to query the similarity of our query document ``query_document`` against every document in the corpus:
        query_words = query_words.lower()
        query_document = query_words.split()

        query_bow = self.dictionary.doc2bow(query_document)
        sims = self.index[self.tfidf[query_bow]]
        # print(list(enumerate(sims)))

        ###############################################################################
        # How to read this output?
        # Document 3 has a similarity score of 0.718=72%, document 2 has a similarity score of 42% etc.
        # We can make this slightly more readable by sorting:
        print('Query: ' + query_words)
        ret = []
        for document_number, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True):
            text_info = self.texts[document_number]
            file = text_info['file']
            text = text_info['text']
            # print(f'Doc Number: {document_number}, Score: {score}, File: {file}, Text: {text}')
            ret_dict = {}
            ret_dict['File'] = file
            ret_dict['Score'] = score
            ret_dict['Text'] = text
            ret.append(ret_dict)

        return ret

# s = SMSSearcher('E:/SW-SysMPy/SysMPy/examples/NotebookExample/Steel Industry')
# print(s.search('are'))
# s = SMSSearcher('Doc')
# s.search('ss')