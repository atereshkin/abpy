import re
import sys

f = file('easylist.txt')

RE_TOK = re.compile('\W')
index = {}



for rul in f.xreadlines():
    tokens = RE_TOK.split(rul)
    for tok in tokens:
        if len(tok) > 3:
            if tok not in index:
                index[tok] = []
            index[tok].append(rul.strip())

def match(url):
    tokens = RE_TOK.split(url)
    for tok in tokens:
        if len(tok) > 3:
            if tok in index:
                for rul in index[tok]:
                    if rule_match(rul, url):
                        print rul

def rule_match(rul, url):
    return rul in url


if __name__ == '__main__':
    match(sys.argv[1])
