import os
import random
import re
import sys
import math

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
    all_pages = corpus.keys()

    # init dist
    distribution = {}.fromkeys(all_pages, (1-damping_factor)/len(all_pages))
    
    # links
    if corpus[page]:
        all_pages = list(corpus[page])

    for l in all_pages:
        distribution[l] += (damping_factor)/len(all_pages)

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    if n < 1:
        return {}
    
    distribution = {}.fromkeys(corpus.keys(), 0)
    page_r = random.choices(list(corpus.keys()))[0]

    for i in range(n):
        distribution[page_r] += 1
        tmp = transition_model(corpus, page_r, damping_factor)
        # choose page in accordance to distribution from transition model
        page_r = random.choices(list(tmp.keys()), tmp.values())[0]
    
    distribution = {page: num_samples/n for page, num_samples in distribution.items()}

    return distribution



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = corpus.keys()
    distribution = {}.fromkeys(corpus.keys(), 1/len(all_pages))
    distribution_delta = {}.fromkeys(corpus.keys(), math.inf)

    while any(delta > 0.001 for delta in distribution_delta.values()):


        for page in distribution.keys():
            
            proba = (1-damping_factor)/len(all_pages)
            
            for link_i, links_page in corpus.items():
                if not links_page:
                    links_page = corpus.keys()
                if page in links_page:
                    proba += damping_factor * distribution[link_i] / len(links_page)

            distribution_delta[page] = abs(proba - distribution[page])
            distribution[page] = proba
    
    return distribution



if __name__ == "__main__":
    main()
