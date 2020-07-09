

class pstr(str):
    def __sub__(self, other):
        result = []
        for c in self:
            if c in other:
                continue
            result.append(c)
        return "".join(result)


