from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity


def extract_sentences_tfidf(verses, top_n=3):
    # Compute TF-IDF matriximport networkx as nx
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(verses)

    # Compute sentence scores as the sum of TF-IDF values
    verse_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()

    # Get indices of top_n sentences
    top_verses_indices = verse_scores.argsort()[-top_n:][::-1]

    # Extract top sentences
    top_verses = [verses[i] for i in top_verses_indices]
    return top_verses


def extract_sentences_textrank(verses, top_n=3):

    # Compute TF-IDF vectors for sentences
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(verses)

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Build graph from similarity matrix
    nx_graph = nx.from_numpy_array(similarity_matrix)

    # Apply PageRank
    scores = nx.pagerank(nx_graph)

    # Rank sentences by score
    ranked_versese = sorted(
        ((scores[i], s) for i, s in enumerate(verses)), reverse=True
    )

    # Extract top_n sentences
    top_verses = [verse for _, verse in ranked_versese[:top_n]]
    return top_verses


if __name__ == "__main__":
    verses = open("bible-esv-formatted.txt").readlines()
    top_verses_tfidf = extract_sentences_tfidf(verses)
    top_verses_textrank = extract_sentences_textrank(verses)
    print("Top verses using TF-IDF:")
    for verse in top_verses_tfidf:
        print(verse)
    print("\nTop verses using TextRank:")
    for verse in top_verses_textrank:
        print(verse)
