from pyspark import SparkContext
import argparse
from operator import add


def degree (input_file, output_file, spark_context):
    """Computes the degree of each node of a graph:
       Inputs:
       - file containing an edge between two nodes per lineSearch
       - SparkContext
       Creates a file of (node, degree of node) pairs"""
    data = spark_context.textFile(input_file)\
                        .map(eval)\
                        .flatMap(lambda (node1, node2): [(node1, 1), (node2, 1)])\
                        .reduceByKey(add)\
                        .collect()

    with open(output_file, 'w') as fh:
        for elem in data:
            print >> fh, elem

def WL (input_file, output_file, spark_context):
    """Computes the WL coloring of each node:
       Inputs:
       - file containing an edge between two nodes per lineSearch
       - SparkContext
       Creates a file of (node, WL coloring) pairs"""
    data = spark_context.textFile(input_file)\
                        .map(eval)\



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'GraphMatch.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('Graph', default=None, help='Input file of edges (node1, node2)')
    parser.add_argument('--outputfile', default='p.out', help='Output file')

    args = parser.parse_args()

    sc = SparkContext(appName='Graph Matching')

    #print 'Computing degree of',args.Graph
    #degree(args.Graph, args.outputfile, sc)
