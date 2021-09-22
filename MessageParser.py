import sys
import MeCab

SEP_CHAR = '\t'
DICT = ''
WORD_CLASS = 4

class MessageParser:

    def __init__(self, sentence):
        self.sentence = sentence
        self.m = MeCab.Tagger()

    def GetNouns(self):
        nouns = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                if "名詞" in analizedData[WORD_CLASS]:
                    nouns.append(analizedData[0])

        return nouns

    def GetVerb(self):
        verb = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            #print("analizedData = " + str(analizedData))
            if len(analizedData) > WORD_CLASS:
                if "動詞" in analizedData[WORD_CLASS]:
                    verb.append(analizedData[0])
        return verb

    def GetNounsData(self):
        nouns = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                if "名詞" in analizedData[WORD_CLASS]:
                    nouns.append(analizedData)

        return nouns

    def GetVerbData(self):
        verb = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                if "動詞" in analizedData[WORD_CLASS]:
                    verb.append(analizedData)

        return verb

    def GetParse(self):
        parse = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                parse.append(analizedData)

        return parse

    def GetSentence(self):
        return self.sentence


if __name__ == "__main__":
    p = MessageParser("エアコンつけて！！")

    print("名詞---")
    print(p.GetNouns())
    print("動詞---")
    print(p.GetVerb())
    print("---")
    print(p.GetParse())
    print(p.GetSentence())
