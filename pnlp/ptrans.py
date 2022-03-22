from typing import List, Tuple


def pick_entity_from_bio_labels(
        pairs: List[Tuple[str, str]]
) -> List[Tuple[str, str]]:
    """
    Parameters
    ----------
    pairs: List of tuple pairs, each pair contains a token and a bio tag

    Returns
    -------
    List of entity pairs, each pair contains an entity and entity type
    """

    def collect(span: List[Tuple[str, str]]):
        res = []
        for c, t in span:
            if t.endswith("O"):
                continue
            res.append(c)
        return "".join(res), span[0][1].split("-")[-1]

    pairs.append(("#", "O"))
    bidx = []
    for i, (c, t) in enumerate(pairs):
        if t.startswith("B-"):
            bidx.append(i)
    bidx.append(len(pairs) - 1)
    res = []
    for i in range(len(bidx) - 1):
        span = pairs[bidx[i]: bidx[i + 1]]
        need = collect(span)
        res.append(need)
    pairs.pop()
    return res
