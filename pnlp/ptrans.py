from typing import List, Tuple
import uuid


def generate_uuid(*args) -> str:
    s = uuid.uuid5(
        uuid.NAMESPACE_URL,
        " ".join(map(str, args))
    )
    return s.hex


def pick_entity_from_bio_labels(
        pairs: List[Tuple[str, str]],
        with_offset: bool = False
) -> List[Tuple[str, str]]:
    """
    Parameters
    ----------
    pairs: List of tuple pairs, each pair contains a token and a bio tag
    with_offset: whether to return locations for the entities

    Returns
    -------
    List of entity pairs, each pair contains an entity and entity type (migtht also a start and end index)
    """

    def collect(span: List[Tuple[str, str]]):
        res = []
        for c, t in span:
            if t.endswith("O"):
                break
            res.append(c)
        return "".join(res), span[0][1].split("-")[-1]

    without_lasto = False
    if pairs and pairs[-1][1] != "O":
        without_lasto = True
        pairs.append(("#", "O"))
    bidx = []
    for i, (c, t) in enumerate(pairs):
        if t.startswith("B-"):
            bidx.append(i)
    bidx.append(len(pairs) - 1)
    res = []
    for i in range(len(bidx) - 1):
        start, end = bidx[i], bidx[i + 1]
        span = pairs[start: end]
        word, tag = collect(span)
        if with_offset:
            tup = (word, tag, start, start + len(word))
        else:
            tup = (word, tag)
        res.append(tup)
    if without_lasto:
        pairs.pop()
    return res
