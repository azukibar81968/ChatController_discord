import sys
import MeCab


class MessageParser:

    def __init__(self, sentence):
        self.sentence = sentence
        self.m = MeCab.Tagger()

    def GetNouns(self):
        nouns = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split('\t')
            if len(analizedData) > 3:
                if "名詞" in analizedData[3]:
                    nouns.append(analizedData[0])

        return nouns

    def GetVerb(self):
        verb = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split('\t')
            if len(analizedData) > 3:
                if "動詞" in analizedData[3]:
                    verb.append(analizedData[0])

        return verb

    def GetNounsData(self):
        nouns = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split('\t')
            if len(analizedData) > 3:
                if "名詞" in analizedData[3]:
                    nouns.append(analizedData)

        return nouns

    def GetVerbData(self):
        verb = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split('\t')
            if len(analizedData) > 3:
                if "動詞" in analizedData[3]:
                    verb.append(analizedData)

        return verb

    def GetParse(self):
        parse = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split('\t')
            if len(analizedData) > 3:
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
