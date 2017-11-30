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

def WLcolor (input_file, output_file, spark_context):
    """Computes the WL coloring of each node:
       Inputs:
       - file containing an edge between two nodes per lineSearch
       - SparkContext
       Creates a file of (node, WL coloring) pairs"""
    #create (node, listof[neighbors]) pairs, both directions
    edges = spark_context.textFile(input_file)\
                             .map(eval)\
                             .flatMap(lambda (node1, node2): [(node1, node2), (node2, node1)])
    #initilize nodes to have a color of 1
    nodeColors = spark_context.textFile(input_file)\
                              .map(eval)\
                              .flatMap(lambda (node1, node2): [(node1, 1), (node2, 1)])\
                              .reduceByKey(lambda (x,y): 1)
    #pass to colors (a recursive function) which returns an RDD of (node, color) pairs
    nodeColors = color(edges, nodeColors, 1).collect()
    with open(output_file, 'w') as fh:
        for elem in nodeColors:
            print >> fh, elem

def color(edges, nodeColors, numOfColors):
    """Computes the WL coloring of each node:
       Inputs:
       - RDD containing (node1, node2) edge pairs
       - RDD containing (node, color) pairs
       Creates an RDD of (node, WL coloring) pairs"""
    #use the Graph-Parallel method as described in lecture 12
    nodeColors = edges.join(nodeColors)\
                      .values()\
                      .combineByKey((lambda x: list(x)),\
                                    (lambda x, y: x.append(y)),\
                                    (lambda x, y: x + y))\
                      .map(lambda (node, colors): (node, hash(sort(colors))))
                      
    checkNumOfColors = nodeColors.values()\
                                 .distinct()\
                                 .count()

    if (checkNumOfColors != numOfColors):
        color(edges, nodeColors, checkNumOfColors)
    else:
        return nodeColors







if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'GraphMatch.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('Graph', default=None, help='Input file of edges (node1, node2)')
    parser.add_argument('--outputfile', default='p.out', help='Output file')

    args = parser.parse_args()

    sc = SparkContext(appName='Graph Matching')

    #print 'Computing degree of',args.Graph
    #degree(args.Graph, args.outputfile, sc)

    print 'Computing coloring of',args.Graph
    WLcolor(args.Graph, args.outputfile, sc)
