import re
import pytest

from pnlp.pcut import cut_sentence, cut_zhchar, combine_bucket


def test_text2zhchar1():
    text = "我喜欢你。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "。"]


def test_text2zhchar2():
    text = "我 喜欢 你。"
    ret = cut_zhchar(text)
    assert ret == ["我", " ", "喜", "欢", " ", "你", "。"]


def test_text2zhchar3():
    text = "我喜欢like你。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "like", "你", "。"]


def test_text2zhchar4():
    text = "我喜欢你233。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "233", "。"]


def test_text2zhchar5():
    text = "我喜欢你3.14。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "3.14", "。"]


def test_text2zhchar6():
    text = "我喜欢你100%。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "100%", "。"]


def test_text2zhchar7():
    text = "我喜欢你2/3。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "2/3", "。"]


def test_text2zhchar8():
    text = "我喜欢你-2。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "-2", "。"]


def test_text2zhchar9():
    text = "我喜欢你2、3。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "2", "、", "3", "。"]


def test_text2zhchar10():
    text = "我喜欢你。。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "。", "。"]


def test_text2zhchar11():
    text = "我喜欢你A-B。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "A", "-", "B", "。"]


def test_text2zhchar12():
    text = "我喜欢你A_B。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "A", "_", "B", "。"]


def test_text2zhchar13():
    text = "我喜欢你C++。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "C", "+", "+", "。"]


def test_text2zhchar14():
    text = "我喜欢你R&B。"
    ret = cut_zhchar(text)
    assert ret == ["我", "喜", "欢", "你", "R", "&", "B", "。"]


def test_text2zhchar15():
    text = "#我喜欢你。"
    ret = cut_zhchar(text)
    assert ret == ["#", "我", "喜", "欢", "你", "。"]


def test_text2zhchar16():
    text = "我 喜欢 你。"
    ret = cut_zhchar(text, remove_blank=True)
    assert ret == ["我", "喜", "欢", "你", "。"]


def test_text2zhchar17():
    text = "我 love you."
    ret = cut_zhchar(text, remove_blank=True)
    assert ret == ["我", "love", "you", "."]


def test_text2zhchar18():
    text = "lo-ve."
    ret = cut_zhchar(text, remove_blank=True)
    assert ret == ['lo', '-', 've', '.']


def test_text2zhchar19():
    text = "v-.f "
    ret = cut_zhchar(text, remove_blank=True)
    assert ret == ['v', '-', '.', 'f']


def test_text2zhchar20():
    text = "-1.2."
    ret = cut_zhchar(text)
    assert ret == ['-1.2', '.']


def test_text2zhchar21():
    text = "1-2-3-"
    ret = cut_zhchar(text)
    assert ret == ['1-2-3-']


def test_text2zhchar22():
    text = "-1-2-3"
    ret = cut_zhchar(text)
    assert ret == ['-1-2-3']


def test_text2zhchar23():
    text = "1.2.3"
    ret = cut_zhchar(text)
    assert ret == ['1.2.3']


def test_text2zhchar24():
    text = "1..2"
    ret = cut_zhchar(text)
    assert ret == ['1..2']


def test_text2zhchar25():
    text = "1.2..."
    ret = cut_zhchar(text)
    assert ret == ['1.2', '.', '.', '.']


def test_text2zhchar26():
    text = "1...2..."
    ret = cut_zhchar(text)
    assert ret == ['1...2', '.', '.', '.']


def test_text2zhchar27():
    text = """
    x..x 1.2, -1.23 lo-.ve.. -1-2-3- 2-2. -1.2. 3/5 1.2.3 1..2 2% 3.5% -2.0%
    """
    ret = cut_zhchar(text, remove_blank=True)
    assert ret == [
        'x', '.', '.', 'x',
        '1.2', ',', '-1.23',
        'lo', '-', '.', 've', '.', '.',
        '-1-2-3-', '2-2', '.',
        '-1.2', '.', '3/5',
        '1.2.3', '1..2',
        '2%', '3.5%', '-2.0%'
    ]


def test_text2sent1():
    text = "我喜欢你，你呢？哈哈，我不告诉你。"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，你呢？"
    assert ret[1] == "哈哈，我不告诉你。"


def test_text2sent2():
    text = "我喜欢你，你呢！哈哈，我不告诉你"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，你呢！"
    assert ret[1] == "哈哈，我不告诉你"


def test_text2sent3():
    text = "我喜欢你，「哈哈」。我不告诉你~~~"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，「哈哈」。"
    assert ret[1] == "我不告诉你~~~"


def test_text2sent4():
    text = "我喜欢你，“哈哈”.我不告诉你……"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，“哈哈”."
    assert ret[1] == "我不告诉你……"


def test_text2sent5():
    text = "我喜欢你，“哈哈” 我不告诉你；"
    ret = cut_sentence(text)
    assert len(ret) == 1
    assert ret[0] == "我喜欢你，“哈哈” 我不告诉你；"


def test_text2sent6():
    text = "我喜欢你，“哈哈。” 我不告诉你!"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你，“哈哈。”"
    assert ret[1] == " 我不告诉你!"


def test_text2sent7():
    text = "我喜欢你(haha). 我不告诉你～"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你(haha)."
    assert ret[1] == " 我不告诉你～"


def test_text2sent8():
    text = "我喜欢你, “哈哈……”。“我不告诉你.”"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你, “哈哈……”。"
    assert ret[1] == "“我不告诉你.”"


def test_text2sent9():
    text = "我喜欢你&“哈哈？”“我不告诉你”"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret[0] == "我喜欢你&“哈哈？”"
    assert ret[1] == "“我不告诉你”"


def test_text2sent10():
    text = "我喜欢你，"
    ret = cut_sentence(text)
    assert len(ret) == 1
    assert ret[0] == "我喜欢你，"


def test_text2sent11():
    text = "我喜欢你"
    ret = cut_sentence(text)
    assert len(ret) == 1
    assert ret[0] == "我喜欢你"


def test_text2sent12():
    text = "我喜欢\n你"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret == ["我喜欢\n", "你"]


def test_text2sent13():
    text = "我喜欢。\n你"
    ret = cut_sentence(text)
    assert len(ret) == 3
    assert ret == ["我喜欢。", "\n", "你"]


def test_text2sent14():
    text = "我喜欢。\n.你"
    ret = cut_sentence(text)
    assert len(ret) == 3
    assert ret == ["我喜欢。", "\n", ".你"]


def test_text2sent15():
    text = "我喜欢\n.你"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret == ["我喜欢\n", ".你"]


def test_text2sent16():
    text = "我喜欢 .你"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret == ["我喜欢 .", "你"]


def test_text2sent17():
    text = "我喜欢　.你"
    ret = cut_sentence(text)
    assert len(ret) == 2
    assert ret == ["我喜欢　.", "你"]


@pytest.fixture
def parts():
    return [
        '习近平指出',
        '中方不仅维护中国人民生命安全和身体健康',
        '也维护世界人民生命安全和身体健康',
        '我们本着公开',
        '透明',
    ]


def test_combine_bucket1(parts):
    ret = combine_bucket(parts.copy(), 5)
    assert ret == parts
    ret = combine_bucket(parts.copy(), 10)
    assert ret == [
        '习近平指出',
        '中方不仅维护中国人民生命安全和身体健康',
        '也维护世界人民生命安全和身体健康',
        '我们本着公开透明',
    ]


def test_combine_bucket2(parts):
    ret = combine_bucket(parts.copy(), 5, truncate=True)
    assert ret == [
        '习近平指出',
        '中方不仅维',
        '也维护世界',
        '我们本着公',
        '透明'
    ]
    ret = combine_bucket(parts.copy(), 10, truncate=True)
    assert ret == [
        '习近平指出',
        '中方不仅维护中国人民',
        '也维护世界人民生命安',
        '我们本着公开透明',
    ]


def test_combine_bucket3(parts):
    ret = combine_bucket(parts.copy(), 5, truncate=True, keep_remain=True)
    assert ret == [
        '习近平指出',
        '中方不仅维',
        '护中国人民',
        '生命安全和',
        '身体健康',
        '也维护世界',
        '人民生命安',
        '全和身体健',
        '康',
        '我们本着公',
        '开',
        '透明'
    ]
    ret = combine_bucket(parts.copy(), 10, truncate=True, keep_remain=True)
    assert ret == [
        '习近平指出',
        '中方不仅维护中国人民',
        '生命安全和身体健康',
        '也维护世界人民生命安',
        '全和身体健康',
        '我们本着公开透明',
    ]
