

class pstr(str):
    def __sub__(self, other):
        result = []
        for c in self:
            if c in other:
                continue
            result.append(c)
        return "".join(result)


def strip_text(text: str, strip: str):
    if strip == "both":
        return text.strip()
    elif strip == "left":
        return text.lstrip()
    elif strip == "right":
        return text.rstrip()
    else:
        return text
