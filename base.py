#The goal is to make a reddit bot that will look at submissions to
#/r/showerthoughts and search for older submissions of the same thing
#if it finds that this submission is posted often, it will reply with
#a summary of older submissions or a search link
#
#Find proper nouns / key words from the title, perform search for those
#1. Sabrina salem
#If you donate blood as a guy and it goes to another guy, you literally fuel his erections.
#

import praw
import nltk
import config
import itertools

red = 0
sub = 0

def init():
    global red
    global sub
    red = praw.Reddit("ShowerPITA v0.1") 
    red.login(config.user, config.password)
    sub = red.get_subreddit('showerthoughts')

def get_dupes(title):
    tok = nltk.word_tokenize(title)
    tagged = nltk.pos_tag(tok)
    proper_nouns = get_proper_nouns(tagged)
    results = []
    if len(proper_nouns) > 1:
        results+=(perform_query(proper_nouns))
        if len(results) > 1:
            return results
        for i in range(len(proper_nouns) - 1, len(proper_nouns)//2,-1):
            if i == 1:
                break
            combinations = itertools.combinations(proper_nouns, i)
            for combination in combinations:
                results+=(perform_query(combination))
            if len(results) > 1:
                return results
    common_nouns = get_common_nouns(tagged) + proper_nouns
    if len(common_nouns) > 1:
        results+=(perform_query(common_nouns))
        if len(results) > 1:
            return results
        for i in range(len(common_nouns) - 1, len(common_nouns)-2, -1):
            if i == 1:
                break
            combinations = itertools.combinations(common_nouns, i)
            for combination in combinations:
                results+=(perform_query(combination))
            if len(results) > 1:
                return results
    return results

def get_proper_nouns(tagged):
    res = []
    for pair in tagged:
        if pair[1] == 'NNP' or pair[1] == 'NNPS':
            res.append(pair[0])
    return res

def get_common_nouns(tagged):
    res = []
    for pair in tagged:
        if pair[1] == 'NN' or pair[1] == 'NNS':
            res.append(pair[0])
    return res

def perform_query(words):
    results = sub.search(" ".join(words))
    x =  [result.title for result in results]
    return x

init()
