import string

import nltk
from nltk import re
from nltk.corpus import stopwords

from helpers import regex, utils


class TwitterPreprocessor:

  def __init__(self, text: str):
    self.text = text

  def fully_preprocess(self):
    return self \
      .remove_urls() \
      .remove_mentions() \
      .remove_hashtags() \
      .remove_twitter_reserved_words() \
      .remove_single_letter_words() \
      .remove_stopwords(extra_stopwords = ['this', 'that', 'the', 'might', 'have', 'been', 'from',
                                           'but', 'they', 'will', 'has', 'having', 'had', 'how', 'went', 'were', 'why', 'and',
                                           'still', 'his', 'her', 'was', 'its', 'per', 'cent', 'a', 'able', 'about', 'across',
                                           'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at',
                                           'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do',
                                           'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has',
                                           'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into',
                                           'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might',
                                           'most', 'must', 'my', 'neither', 'nor', 'not', 'of', 'off', 'often', 'on', 'only',
                                           'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since',
                                           'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they',
                                           'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when',
                                           'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you',
                                           'your', 've', 're', 'rt', 'retweet', '#fuckem', '#fuck', 'fuck', 'ya', 'yall', 'yay',
                                           'youre', 'youve', 'ass', 'factbox', 'com', '&lt', 'th', 'retweeting', 'dick', 'fuckin',
                                           'via', 'hey', 'ooh', 'rt&amp', '&amp', '#retweet', 'retweet', 'goooooooooo', 'hellooo',
                                           'gooo', 'wey', 'sooo', 'helloooooo']) \
      .remove_special_characters() \
      .remove_blank_spaces()

  def remove_urls(self):
    self.text = re.sub(pattern = regex.get_url_patern(), repl = ' ', string = self.text)
    return self

  def remove_special_characters(self):
    self.text = re.sub(pattern = regex.get_special_characters_patern(), repl = ' ', string = self.text)
    return self

  def remove_punctuation(self):
    self.text = self.text.translate(str.maketrans('', '', string.punctuation))
    self.text = self.text.translate(str.maketrans('', '', r"…"))
    return self

  def remove_mentions(self):
    self.text = re.sub(pattern = regex.get_mentions_pattern(), repl = ' ', string = self.text)
    return self

  def remove_hashtags(self):
    self.text = re.sub(pattern = regex.get_hashtags_pattern(), repl = ' ', string = self.text)
    return self

  def remove_twitter_reserved_words(self):
    self.text = re.sub(pattern = regex.get_twitter_reserved_words_pattern(), repl = ' ', string = self.text)
    return self

  def remove_single_letter_words(self):
    self.text = re.sub(pattern = regex.get_single_letter_words_pattern(), repl = ' ', string = self.text)
    return self

  def remove_blank_spaces(self):
    self.text = re.sub(pattern = regex.get_blank_spaces_pattern(), repl = ' ', string = self.text)
    return self

  def remove_stopwords(self, extra_stopwords = None):
    if extra_stopwords is None:
      extra_stopwords = []
    text = nltk.word_tokenize(self.text)
    stop_words = set(stopwords.words('english'))

    new_sentence = []
    for w in text:
      if w not in stop_words and w not in extra_stopwords:
        new_sentence.append(w)
    self.text = ' '.join(new_sentence)
    return self

  def remove_numbers(self, preserve_years = False):
    text_list = self.text.split(' ')
    for text in text_list:
      if text.isnumeric():
        if preserve_years:
          if utils.is_year(text):
            text_list.remove(text)
        else:
          text_list.remove(text)

    self.text = ' '.join(text_list)
    return self
