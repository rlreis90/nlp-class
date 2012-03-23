import sys
import os
import re
import pprint


def cons(xs,v):
    for x in xs: yield x
    yield v

def join(self):
    for xs in self:
        for x in xs:
            yield x
#return [x for xs in xss for x in xs]


""" 
TODO
This function takes in a filename along with the file object (actually
a StringIO object at submission time) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script

NOTE: You shouldn't need to worry about this, but just so you know, the
'file' parameter below will be of type StringIO at submission time. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, file):
  
  gen_pattern = '([\w|\.]+?)(?: \(.*?)?\s*@\s*([\w|\.]+?).edu'
  engler_pattern = '(\w+?) WHERE (\w+?) DOM edu'

  phone_pattern = '(\d{3})(?:-|\s|(?:&thinsp;))(\d{3})(?:-|\s|(?:&thinsp;))(\d{4})'
  
  for line in file:
    for email in re.findall(gen_pattern,line) \
               + re.findall(engler_pattern,line) \
               + [(y, x) for x, y in re.findall('obfuscate\(\'(\w+?).edu\',\'(\w+?)\'\)',line)]:
      yield (name,'e','%s@%s.edu' % email)     
    
    #for email in re.findall('[eE]-?mail(?::| to) (\w+?) at ([\.a-z]+)(?: do?t |\.)([a-z]+)',line):
    #  yield (name,'e','%s@%s.%s' % email)
    #  
    #for email in re.findall('[eE]-?mail(?::| to) (\w+?) at ([\.a-z]+)(?: do?t |\.)([\.a-z]+)(?: do?t \.)([a-z]+)',line):
    #  yield (name,'e','%s@%s.%s.%s' % email)
        
    for email in re.findall('[eE]-?mail(?::| to) (\w+?)(?:\s+|\()at(?:\s+|\))([\.a-z]+)(?: do?t |\.)([\.a-z]+)(?:(?: do?t |\.)([.a-z]+))?',line):
      _, _, _, x = email
      if x != '':
        yield (name,'e','%s@%s.%s.%s' % email)
      else:
        yield (name,'e','%s@%s.%s%s' % email)
        
    
    for phone in re.findall(phone_pattern,line) \
               + re.findall('\((\d{3})\)\s*(\d{3})-(\d{4})',line):
      yield (name,'p','%s-%s-%s' % phone)

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):

    def f(acc, name):
        if name[0] == '.':
            return acc
        else:
            path = os.path.join(data_path, name)
            guesses = process_file(name, open(path,'r'))
            return cons(acc, guesses)

    return join(reduce(f, os.listdir(data_path), []))

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(path):
    # get gold answers
    #gold_list = []
    #f_gold = open(gold_path,'r')
    #for line in f_gold:
    #    gold_list.append(tuple(line.strip().split('\t')))
    #return gold_list

    return reduce(lambda acc, line:
        cons(acc, tuple(line.strip().split('\t'))),
        open(path,'r'),
        [])  

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    #pp.pprint(fn)
    pp.pprint([(x,y,z, [c for (a,b,c) in guess_list if a == x and b == y]) for (x,y,z) in fn])
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))
  
    print ''

"""
You should not need to edit this function. 
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    #if (len(sys.argv) != 3):
    #    print 'usage:\tSpamLord.py <data_dir> <gold_file>'
    #    sys.exit(0)
    #main(sys.argv[1],sys.argv[2])
    
    root = '../data'
    main(root + '/dev', root + '/devGOLD')

