import sys
import argparse
import numpy as np
from pyspark import SparkContext

def toLowerCase(s):
    """ Convert a sting to lowercase. E.g., 'BaNaNa' becomes 'banana'
    """
    return s.lower()

def stripNonAlpha(s):
    """ Remove non alphabetic characters. E.g. 'B:a,n+a1n$a' becomes 'Banana' """
    return ''.join([c for c in s if c.isalpha()])



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Text Analysis through TFIDF computation',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('mode', help='Mode of operation',choices=['TF','IDF','TFIDF','SIM','TOP'])
    parser.add_argument('input', help='Input file or list of files.')
    parser.add_argument('output', help='File in which output is stored')
    parser.add_argument('--master',default="local[20]",help="Spark Master")
    parser.add_argument('--idfvalues',type=str,default="idf", help='File/directory containing IDF values. Used in TFIDF mode to compute TFIDF')
    parser.add_argument('--other',type=str,help = 'Score to which input score is to be compared. Used in SIM mode')
    args = parser.parse_args()

    sc = SparkContext(args.master, 'Text Analysis')


    if args.mode=='TF':
        # Read text file at args.input, compute TF of each term,
        # and store result in file args.output. All terms are first converted to
        # lowercase, and have non alphabetic characters removed
        # (i.e., 'Ba,Na:Na.123' and 'banana' count as the same term). Empty strings, i.e., ""
        # are also removed
        textrdd = sc.textFile(args.input)
        textrdd.flatMap(lambda line: line.split())\
               .map(lambda word: toLowerCase(word))\
               .map(lambda word: stripNonAlpha(word))\
               .map(lambda word: (word, 1))\
               .reduceByKey(lambda val1, val2: val1 + val2)\
               .filter(lambda pair: pair[0] != '')\
               .saveAsTextFile(args.output)


    if args.mode=='TOP':
        # Read file at args.input, comprizing strings representing pairs of the form (TERM,VAL),
        # where TERM is a string and VAL is a numeric value. Find the pairs with the top 20 values,
        # and store result in args.output
        outputfile = open(args.output, 'w')
        textrdd = sc.textFile(args.input)
        top20 = textrdd.flatMap(lambda line: line.split())\
                       .map(lambda word: toLowerCase(word))\
                       .map(lambda word: stripNonAlpha(word))\
                       .map(lambda word: (word, 1))\
                       .reduceByKey(lambda val1, val2: val1 + val2)\
                       .filter(lambda pair: pair[0] != '')\
                       .takeOrdered(20,lambda pair: -pair[1])
        #print each top20 in the given output file
        for element in top20:
            print>>outputfile, element


    if args.mode=='IDF':
        # Read list of files from args.input, compute IDF of each term,
        # and store result in file args.output.  All terms are first converted to
        # lowercase, and have non alphabetic characters removed
        # (i.e., 'Ba,Na:Na.123' and 'banana' count as the same term). Empty strings ""
        # are removed

        #so far makes partitions for word frequency for each word in a document
        dirrdd = sc.wholeTextFiles(args.input)

        num_tf = len(set(dirrdd.keys().collect()))

        dirrdd.flatMapValues(lambda line: line.split())\
              .mapValues(lambda word: toLowerCase(word))\
              .mapValues(lambda word: stripNonAlpha(word))\
              .filter(lambda word: word[1] != '')\
              .map(lambda (tf,word): (word,tf))\
              .combineByKey(lambda tf: [tf],\
                            lambda l, tf: l + [tf],\
                            lambda l1, l2: l1 + l2)\
              .map(lambda (word,l): (word,np.log(num_tf/len(set(l)))))\
              .saveAsTextFile(args.output)


    if args.mode=='TFIDF':
        # Read  TF scores from file args.input the IDF scores from file args.idfvalues,
        # compute TFIDF score, and store it in file args.output. Both input files contain
        # strings representing pairs of the form (TERM,VAL),
        # where TERM is a lowercase letter-only string and VAL is a numeric value.
        wf = sc.textFile(args.input)\
               .map(lambda line: eval(line))

        idf = sc.textFile(args.idfvalues)\
                .map(lambda line: eval(line))

        wf.join(idf)\
          .mapValues(lambda (freq, idf): int(freq)*float(idf))\
          .sortBy(lambda (word, tfidf): -tfidf)\
          .saveAsTextFile(args.output)




    if args.mode=='SIM':
        # Read  scores from file args.input the scores from file args.other,
        # compute the cosine similarity between them, and store it in file args.output. Both input files contain
        # strings representing pairs of the form (TERM,VAL),
        # where TERM is a lowercase, letter-only string and VAL is a numeric value.
        outputfile = open(args.output, 'w')

        tfidf1 = sc.textFile(args.input)\
                   .map(lambda line: eval(line))

        tfidf2 = sc.textFile(args.other)\
                   .map(lambda line: eval(line))

        numerator = tfidf1.join(tfidf2)\
                          .values()\
                          .map(lambda (tfidf1_val, tfidf2_val): tfidf1_val*tfidf2_val)\
                          .reduce(lambda val1, val2: val1+val2)

        tfidf1_sumsq = tfidf1.values()\
                             .map(lambda val: val**2)\
                             .reduce(lambda val1, val2: val1+val2)

        tfidf2_sumsq = tfidf2.values()\
                             .map(lambda val: val**2)\
                             .reduce(lambda val1, val2: val1+val2)

        print>>outputfile, numerator/np.sqrt(tfidf1_sumsq*tfidf2_sumsq)
