
def reciprocal_rank_fusion(rankings, k=60, top_k=5):
    """
    Combine ranked lists of chunk IDs using RRF.

    rankings:
        List of ranked lists.
        Example:
        [
            ["cart.py::A", "cart.py::B"],
            ["cart.py::B", "cart.py::A"]
        ]
    """
    if k < 0:
        raise ValueError("k must be non-negative")

    if top_k <= 0:
        raise ValueError("top_k must be positive")

    scores = {}

    for ranking in rankings:
        for rank, chunk_id in enumerate(ranking, start=1):
            scores[chunk_id] = (
                scores.get(chunk_id, 0.0)
                + 1.0 / (k + rank)
            )

    sorted_results = sorted(
        scores.items(),
        key=lambda item: (-item[1], item[0])
    )

    return [
        {
            "chunk_id": chunk_id,
            "score": score
        }
        for chunk_id, score in sorted_results[:top_k]
    ]
