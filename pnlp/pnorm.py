from dataclasses import dataclass
from typing import TypeVar


T = TypeVar('T', str, float, int)

ZH_NUM = {
    '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5,
    '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
}

ZH_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 10000000000000,
}


ARB_NUM = {
    0: "零",
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
    10: "十",
    100: "百",
    1000: "千",
    10000: "万",
    100000000: "亿",
    10000000000000: "兆"
}

ZH2MONEY = {
    "一": "壹",
    "二": "贰",
    "三": "叁",
    "四": "肆",
    "五": "伍",
    "六": "陆",
    "七": "柒",
    "八": "捌",
    "九": "玖",
    "十": "拾",
    "百": "佰",
    "千": "仟",
    "万": "萬",
    "亿": "億"
}


class pnumstr(str):

    def to_money(self):
        for c in self:
            mc = ZH2MONEY.get(c)
            if mc:
                self = self.replace(c, mc)
        return self


@dataclass
class NumNorm:
    """
    Chinese_to_Arabic
    modifed from https://github.com/bamtercelboo/corpus_process_script/blob/master/cn_to_arabic/cn_to_arabic.py
    """
    @staticmethod
    def num_len(num: int) -> int:
        if num == 0:
            return 1
        if num < 0:
            num = -num
        i = 0
        while num != 0:
            num //= 10
            i += 1
        return i

    def num2zh(self, num: int) -> str:
        def get_base(num):
            zh = ARB_NUM.get(num)
            if num < 10:
                return zh
            else:
                return "一" + zh

        def get_less_than_10w(num):
            res = ""
            while num != 0:
                if num < 10:
                    res += ARB_NUM.get(num)
                    break
                length = NumNorm.num_len(num)
                divider = 10 ** (length - 1)
                high = num // divider
                res += ARB_NUM.get(high)
                res += ARB_NUM.get(divider)
                num = num % divider
                new_len = NumNorm.num_len(num)
                if length - new_len > 1 and num != 0:
                    res += "零"
            return res

        def get_interval(num: int, lower: int, unit: str):
            res = ""
            length = NumNorm.num_len(num)
            divider = lower / 10
            high = num // divider
            res = get_less_than_10w(high)
            high_len = NumNorm.num_len(high)
            res += unit
            num -= high * divider
            new_len = NumNorm.num_len(num)
            if length - high_len - new_len > 0 and num != 0:
                res += "零"
            return res, num

        def get_10w_to_1y(num):
            res, num = get_interval(num, 10**5, "万")
            if 0 < num < 100000:
                res += get_less_than_10w(num)
            return res

        def get_1y_to_1z(num):
            res, num = get_interval(num, 10**9, "亿")
            if 0 < num < 100000000:
                res += get_10w_to_1y(num)
            return res

        if num in ARB_NUM:
            result = get_base(num)
            return pnumstr(result)
        # 十万
        if num < 10**5:
            result = get_less_than_10w(num)
        # 一亿
        elif num < 10**8:
            result = get_10w_to_1y(num)
        # 一兆
        elif num < 10**13:
            result = get_1y_to_1z(num)
        else:
            result = "超大"
        return pnumstr(result)

    def zh2num(self, zh: str) -> T:
        unit = 0
        digit_list = []
        for zhdigit in reversed(zh):
            if zhdigit in ZH_UNIT:
                unit = ZH_UNIT.get(zhdigit)
                if unit == 10000 or unit == 100000000:
                    digit_list.append(unit)
                    unit = 1
            else:
                digit = ZH_NUM.get(zhdigit)
                if unit:
                    digit *= unit
                    unit = 0
                digit_list.append(digit)
        if unit == 10:
            digit_list.append(10)
        val, tmp = 0, 0
        for x in reversed(digit_list):
            if x == 10000 or x == 100000000:
                val += tmp * x
                tmp = 0
            else:
                tmp += x
        val += tmp
        if val == 0 and zh != "零":
            return zh
        else:
            return val
