import os
import random
import re
import sys

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
    distribution = {}
    n = len(corpus)
    
    if corpus[page]:
        for p in corpus:
            distribution[p] = (1 - damping_factor) / n
        
        for link in corpus[page]:
            distribution[link] += damping_factor / len(corpus[page])
    else:
        for p in corpus:
            distribution[p] = 1 / n
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {page: 0 for page in corpus}
    
    current = random.choice(list(corpus.keys()))
    ranks[current] += 1
    
    for _ in range(n - 1):
        probs = transition_model(corpus, current, damping_factor)
        pages = list(probs.keys())
        weights = [probs[p] for p in pages]
        current = random.choices(pages, weights=weights)[0]
        ranks[current] += 1
    
    return {page: rank / n for page, rank in ranks.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    ranks = {page: 1 / n for page in corpus}
    
    modified_corpus = corpus.copy()
    for page, links in corpus.items():
        if not links:
            modified_corpus[page] = set(corpus.keys())
    
    while True:
        new_ranks = {}
        max_change = 0
        
        for page in corpus:
            new_rank = (1 - damping_factor) / n
            
            for linking_page, links in modified_corpus.items():
                if page in links:
                    new_rank += damping_factor * ranks[linking_page] / len(links)
            
            new_ranks[page] = new_rank
            max_change = max(max_change, abs(new_ranks[page] - ranks[page]))
        
        ranks = new_ranks
        
        if max_change < 0.001:
            break
    
    return ranks


if __name__ == "__main__":
    main()
