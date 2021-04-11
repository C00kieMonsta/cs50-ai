import nltk
import sys
import os
import string
import math

nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


# (1) document retrieval and (2) passage retrieval
#   (1) document retrieval will first identify which document(s) are most relevant to the query
#   (2) Once the top documents are found, the top document(s) will be subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    mapping = dict()
    for f_name in os.listdir(directory):
        with open(os.path.join(directory, f_name)) as f:
            mapping[f_name] = f.read()
    return mapping


def is_usable(word):
    return word not in nltk.corpus.stopwords.words("english") and word not in string.punctuation

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document.lower())
    processed_words = []
    for word in words:
        if is_usable(word):
            processed_words.append(word)
    return processed_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_idf = dict()
    num_doc = len(list(documents.keys()))

    for key in documents:
        all_words = set()

        for word in documents[key]:
            if word not in all_words:
                all_words.add(word)
                try:
                    word_idf[word] += 1
                except KeyError:
                    word_idf[word] = 1

    return {word: math.log(num_doc / word_idf[word]) for word in word_idf}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    sorted_files = list()

    for filename in files:
        
        # [1]: matching words
        file_value = [filename, 0]
        for word in query:
            file_value[1] += files[filename].count(word) * idfs[word]
    
        sorted_files.append(file_value)

    return [filename for filename, mwm in sorted(sorted_files, key=lambda item: item[1], reverse=True)][:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sorted_sentences = list()

    for sentence in sentences:

        # [1]: matching words
        # [2]: term density
        sentence_values = [sentence, 0, 0]

        for word in query:
            # check if word in sentence
            if word in sentences[sentence]:
                sentence_values[1] += idfs[word]
                sentence_values[2] += sentences[sentence].count(word) / len(sentences[sentence])

        sorted_sentences.append(sentence_values)
    
    # sort according to idf and then according to term density
    return [sentence for sentence, mwm, qtd in sorted(sorted_sentences, key=lambda item: (item[1], item[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
