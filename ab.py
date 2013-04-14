import re
import sys

f = file('easylist.txt')

RE_TOK = re.compile('\W')
index = {}


MAP_RE = (('\|\|','(//|\.)'),
          ('\^', r'[/\\:+!@#\$^\^&\*\(\)\|]'))

class RuleSyntaxError(Exception):
    pass

class Rule(object):
    def __init__(self, rule_str):
        self.rule_str = rule_str.strip()
        if '$' in rule_str:
            try:
                self.pattern, self.optstring = rule_str.split('$')
            except ValueError:
                raise RuleSyntaxError()
        else:
            self.pattern = self.rule_str
        self.regex = self._to_regex()

    def get_tokens(self):
        return RE_TOK.split(self.pattern)

    def match(self, url):
        return self.regex.search(url)

    def _to_regex(self):
        re_str = re.escape(self.pattern)
        for m in MAP_RE:
            re_str = re_str.replace(*m)
        return re.compile(re_str)
    
    def __unicode__(self):
        return self.rule_str

for rul in f.xreadlines():
    if rul.startswith('##'):
        continue
    try:
        rule = Rule(rul)
    except RuleSyntaxError:
        print 'syntax error in ', rul
    for tok in rule.get_tokens():
        if len(tok) > 2:
            if tok not in index:
                index[tok] = []
            index[tok].append(rule)

def match(url):
    tokens = RE_TOK.split(url)
    for tok in tokens:
        if len(tok) > 2:
            if tok in index:
                for rule in index[tok]:
                    if rule.match(url):
                        print unicode(rule)


if __name__ == '__main__':
    print 'start matching'
    match(sys.argv[1])
