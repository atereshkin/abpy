import re
import sys


RE_TOK = re.compile('\W')


MAP_RE = (('\|\|','(//|\.)'),
          ('\^', r'[/\\:+!@#\$^\^&\*\(\)\|]'),
          ('\*', r'.*'))

class RuleSyntaxError(Exception):
    pass

TYPE_OPTS = (('script', 'external scripts loaded via HTML script tag'),
             ('image', 'regular images, typically loaded via HTML img tag'),
             ('stylesheet', 'external CSS stylesheet files'),
             ('object', 'content handled by browser plugins, e.g. Flash or Java'),
             ('xmlhttprequest', 'requests started by the XMLHttpRequest object'),
             ('object-subrequest', 'requests started plugins like Flash'),
             ('subdocument', 'embedded pages, usually included via HTML frames'),
             ('document', 'the page itself (only exception rules can be applied to the page)'),
             ('elemhide', 'for exception rules only, similar to document but only disables element hiding rules on the page rather than all filter rules (Adblock Plus 1.2 and higher required)'),
             ('other', 'types of requests not covered in the list above'))
TYPE_OPT_IDS = [x[0] for x in TYPE_OPTS]

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
            self.optstring = ''
        self.regex = self._to_regex()
        opts = self.optstring.split(',')
        self.excluded_elements = []
        self.matched_elements = []
        for o in opts:
            if o.startswith('~') and o[1:] in TYPE_OPT_IDS:
                self.excluded_elements.append(o)
            elif o in TYPE_OPT_IDS:
                self.matched_elements.append(o)
        if self.matched_elements == []:
            self.matched_elements = TYPE_OPT_IDS

    def get_tokens(self):
        return RE_TOK.split(self.pattern)

    def match(self, url, elementtype=None):
        if elementtype:
            if elementtype in self.excluded_elements or\
                    (elementtype not in self.matched_elements and\
                         'other' not in self.matched_elements):
                return False
        return self.regex.search(url)

    def _to_regex(self):
        re_str = re.escape(self.pattern)
        for m in MAP_RE:
            re_str = re_str.replace(*m)
        return re.compile(re_str)
    
    def __unicode__(self):
        return self.rule_str


class Filter(object):
    def __init__(self, f):
        self.index = {}
        for rul in f.xreadlines():
            if rul.startswith('!'): # Comment 
                continue 
            if '##' in rul: # HTML rule
                continue
            try:
                rule = Rule(rul)
            except RuleSyntaxError:
                print 'syntax error in ', rul
            for tok in rule.get_tokens():
                if len(tok) > 2:
                    if tok not in self.index:
                        self.index[tok] = []
                    self.index[tok].append(rule)

    def match(self, url, elementtype=None):
        tokens = RE_TOK.split(url)
        for tok in tokens:
            if len(tok) > 2:
                if tok in self.index:
                    for rule in self.index[tok]:
                        if rule.match(url, elementtype=elementtype):
                            print unicode(rule)


if __name__ == '__main__':
    f = Filter(file('easylist.txt'))
    print 'start matching'
    f.match(sys.argv[1])
