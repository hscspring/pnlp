import pytest

from pnlp.ptrans import pick_entity_from_bio_labels, generate_uuid


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


@pytest.mark.parametrize("pairs,result", [
    ([("我", "O"), ("国", "O"), ("北", "B-LOC"), ("京", "I-LOC")], [("北京", "LOC", 2, 4)]),
    ([("我", "O"), ("国", "O"), ("北", "B-LOC"), ("京", "I-LOC"), ("。", "O")], [("北京", "LOC", 2, 4)]),
    ([("我", "O"), ("国", "O"), ("北", "B-LOC"), ("京", "I-LOC"), ("天", "B-LOC"), ("安", "I-LOC"), ("门", "I-LOC")], [("北京", "LOC", 2, 4), ("天安门", "LOC", 4, 7)]),
    ([("我", "O"), ("国", "O"), ("北", "B-LOC"), ("京", "I-LOC"), ("的", "O"), ("天", "B-LOC"), ("安", "I-LOC"), ("门", "I-LOC")], [("北京", "LOC", 2, 4), ("天安门", "LOC", 5, 8)]),
    ([("北", "B-LOC"), ("京", "I-LOC"), ("天", "B-LOC"), ("安", "I-LOC"), ("门", "I-LOC")], [("北京", "LOC", 0, 2), ("天安门", "LOC", 2, 5)]),
    ([("北", "B-LOC"), ("京", "I-LOC"), ("天", "B-LOC"), ("安", "I-LOC"), ("门", "I-LOC"), ("。", "O")], [("北京", "LOC", 0, 2), ("天安门", "LOC", 2, 5)]),
    ([("北", "B-ORG"), ("大", "I-ORG"), ("蔡", "B-PER"), ("元", "I-PER"), ("培", "I-PER")], [("北大", "ORG", 0, 2), ("蔡元培", "PER", 2, 5)]),
    ([("说", "O"), ("北", "B-ORG"), ("大", "I-ORG"), ("蔡", "B-PER"), ("元", "I-PER"), ("培", "I-PER")], [("北大", "ORG", 1, 3), ("蔡元培", "PER", 3, 6)]),
    ([("北", "B-ORG"), ("大", "I-ORG"), ("蔡", "B-PER"), ("元", "I-PER"), ("培", "I-PER"), ("啊", "O")], [("北大", "ORG", 0, 2), ("蔡元培", "PER", 2, 5)]),
    ([("北", "B-LOC"), ("京", "I-LOC"), ("的", "O"), ("安", "I-LOC")], [("北京", "LOC", 0, 2)]),
    ([("北", "B-LOC"), ("京", "I-LOC"), ("的", "O"), ("安", "B-LOC")], [("北京", "LOC", 0, 2), ("安", "LOC", 3, 4)]),
])
def test_pick_entity_from_bio_labels_with_offset(pairs, result):
    entities = pick_entity_from_bio_labels(pairs, True)
    assert entities == result


@pytest.mark.parametrize("inp", [
    (("a", 1, 0.5)),
    (("好", 1, 0.5)),
])
def test_generate_uuid(inp):
    uid = generate_uuid(*inp)
    assert type(uid) == str
    assert len(uid) == 32
