import pytest

from pnlp.ptrans import pick_entity_from_bio_labels


@pytest.mark.parametrize("pairs,result", [
    ([('v1', 'B-1')], [("v1", "1")]),
    ([('v0', 'O'), ('vo', 'O')], []),
    ([('v1', 'B-1'), ('v2', 'I-1')], [("v1v2", "1")]),
    ([('v1', 'B-1'), ('v2', 'I-1'), ('v0', 'O')], [("v1v2", "1")]),
    ([('v1', 'O'),
      ('v2', 'B-2'),
      ('v3', 'B-3'),
      ('v4', 'I-3'),
      ('v5', 'B-5'),
      ('v6', 'B-6'),
      ('v0', 'O'),
      ('v0', 'O'),
      ('v7', 'B-7'),
      ('v8', 'I-7'),
      ('v9', 'B-9')],
     [("v2", "2"), ("v3v4", "3"), ("v5", "5"), ("v6", "6"), ("v7v8", "7"), ("v9", "9")]
     ),
])
def test_pick_entity_from_bio_labels(pairs, result):
    entities = pick_entity_from_bio_labels(pairs)
    assert entities == result
