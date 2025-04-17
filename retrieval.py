from rank_bm25 import BM25Okapi


def bm25_test():
    """
    https://pypi.org/project/rank-bm25/
    """

    # First thing to do is create an instance of the BM25 class, which reads in a corpus of text and does some indexing on it:
    # Note that this package doesn't do any text preprocessing. If you want to do things like lowercasing, stopword removal, stemming, etc, you need to do it yourself.
    corpus = [
        "Hello there good man!",
        "It is quite windy in London",
        "How is the weather today?"
    ]
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)

    # Good to note that we also need to tokenize our query, and apply the same preprocessing steps we did to the documents in order to have an apples-to-apples comparison
    query = "windy London"
    tokenized_query = query.split(" ")

    # Now that we've created our document indexes, we can give it queries and see which documents are the most relevant:
    doc_scores = bm25.get_scores(tokenized_query)

    # Instead of getting the document scores, you can also just retrieve the best documents with
    contexts = bm25.get_top_n(tokenized_query, corpus, n=3)

    print(doc_scores)
    print(contexts)


def main():
    print("bm25")
    bm25_test()


if __name__ == "__main__":
    main()
