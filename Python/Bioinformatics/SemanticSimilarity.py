# Assignment 2 - CSC-571 - Dr. Pranshanti Manda - UNCG
#
# Calculates the Semantic Similarity between input genes
# using Resnik and Jaccard functions
#
# @author: James Knox Polk <jkpolk@uncg.edu>
# Last Revision: 2/28/2019

import math


def build_inferred(gene):
    inferred_set = set()
    with open("JPolk_GO.tsv") as fd:
        go_dict = dict([line.split("\t") for line in fd])
    if isinstance(gene, tuple):
        for x in gene:
            inferred_set.add(x)
            for y in go_dict[x].rstrip().split(","):
                inferred_set.add(y)
    else:
        inferred_set.add(gene)
        for y in go_dict[gene].rstrip().split(","):
            inferred_set.add(y)

    return inferred_set


def get_jaccard(set1, set2):
    u = set1 | set2
    i = set1 & set2
    return len(i)/len(u)


def get_resnik(set1, set2):
    ic_scores = []
    superset = set1 & set2
    if len(superset) == 0:
        return 0

    for x in superset:
        ic_scores.append(-math.log(ic_dict[x]/3))

    return max(ic_scores)


def get_all_pairs(gene1, gene2, method):
    scores = []

    if method is "jaccard":
        if isinstance(gene1, tuple):
            if isinstance(gene2, tuple):
                for x, y in gene1, gene2:
                    set1 = build_inferred(x)
                    set2 = build_inferred(y)
                    scores.append(get_jaccard(set1, set2))
            else:
                for x in gene1:
                    set1 = build_inferred(x)
                    set2 = build_inferred(gene2)
                    scores.append(get_jaccard(set1, set2))
        else:
            if isinstance(gene2, tuple):
                for x in gene2:
                    set1 = build_inferred(x)
                    set2 = build_inferred(gene1)
                    scores.append(get_jaccard(set1, set2))
            else:
                set1 = build_inferred(gene1)
                set2 = build_inferred(gene2)
                scores.append(get_jaccard(set1, set2))

    if method is "resnik":
        if isinstance(gene1, tuple):
            if isinstance(gene2, tuple):
                for x, y in gene1, gene2:
                    set1 = build_inferred(x)
                    set2 = build_inferred(y)
                    scores.append(get_resnik(set1, set2))
            else:
                for x in gene1:
                    set1 = build_inferred(x)
                    set2 = build_inferred(gene2)
                    scores.append(get_resnik(set1, set2))
        else:
            if isinstance(gene2, tuple):
                for x in gene2:
                    set1 = build_inferred(x)
                    set2 = build_inferred(gene1)
                    scores.append(get_resnik(set1, set2))
            else:
                set1 = build_inferred(gene1)
                set2 = build_inferred(gene2)
                scores.append(get_resnik(set1, set2))

    return sum(scores)/len(scores)


def get_best_pairs(gene1, gene2, method):
    bp_scores = []
    scores = []
    result = get_all_pairs(gene1, gene2, method)
    if isinstance(gene1, tuple):
        if isinstance(gene2, tuple):
            for x in gene1:
                scores.clear()
                for y in gene2:
                    set1 = build_inferred(x)
                    set2 = build_inferred(y)
                    if method is "jaccard":
                        scores.append(get_jaccard(set1, set2))
                    if method is "resnik":
                        scores.append(get_resnik(set1, set2))
                bp_scores.append(max(scores))
            result = sum(bp_scores)/len(bp_scores)

    return result


def get_ic_dict(gene1, gene2, gene3):
    genes = dict()
    # Get the IC of each of the superclasses and build a dictionary of the unions
    for x in gene1:
        genes[x] = 1

    for y in gene2:
        if y in genes.keys():
            y_value = genes.pop(y)
            genes[y] = y_value + 1
        else:
            genes[y] = 1

    for z in gene3:
        if z in genes.keys():
            z_value = genes.pop(z)
            genes[z] = z_value + 1
        else:
            genes[z] = 1

    return genes


geneA = ("GO_0016020", "GO_0003677")
geneB = "GO_0016021"
geneC = "GO_0003677"

geneA_set = build_inferred(geneA)
geneB_set = build_inferred(geneB)
geneC_set = build_inferred(geneC)

ic_dict = get_ic_dict(geneA_set, geneB_set, geneC_set)


print("\nAll Pairs Jaccard for A and C: ", get_all_pairs(geneA, geneC, "jaccard"))
print("\nBest Pairs Jaccard for A and C: ", get_best_pairs(geneA, geneC, "jaccard"))
print("\nBest Pairs Resnik for A and B: ", get_best_pairs(geneA, geneB, "resnik"))
