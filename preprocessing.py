#coding=utf8
'''
    preprocessing data for the experiments
'''
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re
from str_util import unicode2str, str2unicode
from yelp_extractor import extract_from_json

yelp_dir = 'data/yelp/'

def lda_pre():
    '''
        preprocessing texts for LDA model,
        remove numbers, tokenization, stopwords removal, stemming
        save processed text into db
    '''
    reviews = extract_from_json('review')
    id2raw, id2prew = {}, {}
    #lines = open(yelp_dir+filename, 'r').readlines()
    #parts = [l.strip().split('\t') for l in lines if not l.startswith('#')]
    #texts = [str2unicode(p[3]) for p in parts]

    tokenizer = RegexpTokenizer(r'\w+')
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    # create English stop words list
    en_stop = get_stop_words('en')

    wfilename = 'raw_reviews.ldapre'
    fw = open(yelp_dir+wfilename, 'w+')
    fw.write('#review_id\trate\tprocessed_text\n')
    for ind, r in enumerate(reviews):
        if (ind+1) % 100000 == 0:
            print 'processing %s/%s' % (ind+1,len(reviews))
        text = r['text']
        rid = r['review_id']
        rate = r['stars']
        #remove numbers
        text = re.sub(r'\d+', '', text)
        #remove \n
        text = re.sub(r'\n', ' ', text)

        #text = str2unicode(text)

        # clean and tokenize document string
        tokenized_text = tokenizer.tokenize(text.lower())

        # remove stop words from tokens
        stopped_tokens = [i for i in tokenized_text if not i in en_stop]

        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        p_text = '\t'.join(stemmed_tokens)
        r['processed_text'] = p_text
        parts = [unicode2str(rid), str(rate), unicode2str(p_text)]
        fw.write('%s\n' % '\t'.join(parts))
    fw.close()
    print 'finish preprocessing, res saved in %s' % wfilename

def get_user_average_rate():
    reviews = extract_from_json('review')
    uid2rates = {}
    for rev in reviews:
        uid = rev['user_id']
        rate = rev['stars']
        uid2rates.setdefault(uid,[]).append(rate)
    uid2rates = [(uid, sum(rates) * 1.0 / len(rates)) for uid, rates in uid2rates.items()]
    filename = 'user_avg_rate.txt'
    fw = open(yelp_dir+filename, 'w+')
    fw.write('\n'.join(['%s\t%s' % (uid,round(avg,2)) for uid,avg in uid2rates]))


if __name__ == '__main__':
    get_user_average_rate()
