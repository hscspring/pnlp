from collections import Counter


class MagicDict(dict):

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            # create a self instance
            value = self[item] = type(self)()
            return value

    @staticmethod
    def reverse(dic):
        """
        Preserve all repeated value-keys when a Dict is reversed.

        Parameters
        ----------
        dic: dict
            A dict where several keys have the same values.

        Returns
        -------
        Reversed dict of the given dict, but preserve all key-values.

        Example
        -------
        dx = {  1: 'a',
                2: 'a',
                3: 'a',
                4: 'b' }
        reversedx = {   'a': [1, 2, 3],
                        'b': 4 }
        """
        d1 = dict(zip(dic.values(), [[] for i in range(len(dic))]))
        d2 = dict([
            (y, d1[y].append(x))
            if y in
            [w for (w, f) in Counter(dic.values()).items() if f > 1]
            else (y, x)
            for (x, y) in dic.items()])
        reversdict = dict([(x, d1[x]) if len(d1[x]) != 0
                           else (x, d2[x])
                           for x in d1.keys()])
        return reversdict
