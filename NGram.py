#!/usr/bin/python
#-*- coding:utf-8 -*-

class NGram(object):
    def __init__(self, text, name="", n=3):
        self.length = None
        self.n = n
        self.table = {}
        self.parse_text(text)
        self.name = name
        self.calculate_length()

    def parse_text(self, text):
        chars = ' ' * self.n    #initial sequence of spaces with length n

        for letter in (" ".join(text.split()) + " "):
        #for letter in text:
            chars = chars[1:] + letter  # append letter to sequence of length n
            self.table[chars] = self.table.get(chars, 0) + 1    #increment count

    def calculate_length(self):
        self.length = sum([x * x for x in self.table.values()]) ** 0.5
        return self.length

    def __sub__(self, other):
        if not isinstance(other, NGram):
            raise TypeError("Can't compare NGram with non-NGram object.")

        if self.n != other.n:
            raise TypeError("Can't compare NGram objects of different size.")

        total = 0
        for k in self.table:
            total += self.table[k] * other.table.get(k, 0)

        # similarity is the inner product of the two NGram 
        # distance is 1.0 minus similarity
        return 1.0 - (float(total)/(float(self.length) * float(other.length)))
    
    # return the best match NGram; The name of the NGram object is the language name
    def find_match(self, languages):
        return min(languages, key=lambda n: self - n)

        """
        target = None
        minv = 1.0
        for lag in languages:
            print lag.name
            #print lag.table
            if self.__sub__(lag) <= minv:
                minv = self - lag
                target = lag
        return target
        """

    def __str__(self):
        return self.name

if __name__ == "__main__":
    nobj = NGram("Snail Mail. I have lunch, are you ok?")
    nobj.calculate_length()

    # Language text test set
    english_text = "I have lunch. Are you ok? Fine. I will go out for supper."
    chinese_text = "This, 你好，我要出去吃饭了，有什么事吗？那你等会儿吧，下午再说"
    japanese_text = "女性が牛乳を飲んだ"
    english = NGram(english_text, 'E')
    print "name ",english
    chinese = NGram(chinese_text, 'C')
    japanese = NGram(japanese_text, 'J')
    languages = [english, chinese, japanese]
    english2 = NGram("kiddingmu. Are you late?")
    # Test NGram override sub method
    print english - english2

    bestfunc = nobj.find_match(languages)
    print "most similar language is:", bestfunc.name

    japantext = "2014明けましておめでとうございます！"
    japanobj = NGram(japantext)
    bestmatch = japanobj.find_match(languages)
    print "most similar language is:", bestmatch.name

    """
    # Test min, lambda syntax
    ilist = [1,2,3,4,5,6]
    print "Generator syntax:", min(i for i in ilist)
    print min(ilist, key=lambda n: 10-n)
    #print min(ilist, lambda n: 10-n)(2)
    """
