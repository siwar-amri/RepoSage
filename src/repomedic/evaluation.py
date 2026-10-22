
def recall_at_k(retrieved, relevant, k):
    if k <= 0:
        raise ValueError("k must be positive")

    if not relevant:
        return 0.0

    top_k = set(retrieved[:k])
    relevant_set = set(relevant)

    found = top_k.intersection(relevant_set)

    return len(found) / len(relevant_set)


def reciprocal_rank(retrieved, relevant):
    relevant_set = set(relevant)

    for rank, function_name in enumerate(retrieved, start=1):
        if function_name in relevant_set:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(rankings, ground_truths):
    if len(rankings) != len(ground_truths):
        raise ValueError("Rankings and ground truths must align")

    if not rankings:
        return 0.0

    scores = [
        reciprocal_rank(retrieved, relevant)
        for retrieved, relevant in zip(rankings, ground_truths)
    ]

    return sum(scores) / len(scores)







    