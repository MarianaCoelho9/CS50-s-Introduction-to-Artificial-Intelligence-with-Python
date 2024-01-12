import os
from queue import Empty
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability={}
    if corpus[page]:


        p_others=(1-damping_factor)/len(corpus.keys())
        p_link=p_others + damping_factor*(1/len(corpus[page]))

        for i in corpus.keys():
            if not(i in corpus[page]):
                probability[i]=p_others
            else:
                probability[i]=p_link
    
    else:
        for i in corpus.keys():
            probability[i]=1/len(corpus.keys())

    return probability

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_rank = {}
    for page in corpus:
        sample_rank[page] = 0
    
    page = random.choice(list(corpus.keys()))

    for i in range(1, n):
        distribution = transition_model(corpus, page, damping_factor)
        for page in sample_rank:
            sample_rank[page] = ((i-1) * sample_rank[page] + distribution[page]) / i
        
        page = random.choices(list(sample_rank.keys()), list(sample_rank.values()), k=1)[0]

    return sample_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N=len(corpus)
    threshold=1
    iterate_rank={}
    for i in corpus.keys():
            iterate_rank[i]=1/N
 
    while threshold>0.001:
        probability_page={}
        for i in corpus.keys():
            probability_page[i]=pagerank(i, corpus, damping_factor, iterate_rank)
        dif=abs(np.subtract(list(probability_page.values()),list(iterate_rank.values())))
        iterate_rank=probability_page
        if dif.max()<threshold:
            threshold=dif.max()

    return iterate_rank

def pagerank(key, corpus, damping_factor,pr):

    pagerank={}
    sum=0
    for page in corpus:
        if key in corpus[page]:
            sum+=pr[page]/len(corpus[page])
    pagerank=((1-damping_factor)/len(corpus))+damping_factor*sum

    return pagerank

if __name__ == "__main__":
    main()
