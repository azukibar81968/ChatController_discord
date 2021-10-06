# -*- coding: utf-8 -*-

import sys
import MeCab
import CaboCha

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

##########CaBoChaラッパー#############

    def gen_chunks(self, tree):
        """
        構文木treeからチャンクの辞書を生成する
        """
        chunks = {}
        key = 0  # intにしているがこれはChunk.linkの値で辿れるようにしている

        for i in range(tree.size()):  # ツリーのサイズだけ回す
            tok = tree.token(i)  # トークンを得る
            if tok.chunk:  # トークンがチャンクを持っていたら
                chunks[key] = tok.chunk  # チャンクを辞書に追加する
                key += 1

        return chunks

    def find_pos(self, toks, pos):
        """
        posの品詞を持つトークンを探す
        """
        for tok in toks:
            if pos in tok.feature.split(','):
                return tok
        return None

    
    def get_surface_from_toks(self, toks):
        """
        トークン列の表層形をまとめる
        """
        surface = ''
        for tok in toks:
            surface += tok.surface
        return surface

    def get_toks_by_chunk(self, tree, chunk):
        """
        チャンクからトークン列を得る
        """
        beg = chunk.token_pos
        end = chunk.token_pos + chunk.token_size
        toks = []

        for i in range(beg, end):
            tok = tree.token(i)
            toks.append(tok)

        return toks


    def analyze_verb_pronoun_relation(self, tree, chunks, chunk):
        print(tree.toString(CaboCha.FORMAT_XML))
        # 引数chunkからトークン列を得る
        verb_toks = self.get_toks_by_chunk(tree, chunk)
        if not len(verb_toks):
            return "NONE: no token list"

        # トークン列から動詞トークンを探す
        verb_tok = self.find_pos(verb_toks, '動詞')
        if not verb_tok:  # 見つからなかった
            return "NONE: no verb token"
        if not verb_tok.chunk:
            return "NONE: chunk unavailable"
        if verb_tok.chunk.link < 0:  # チャンクにリンクがない
            return "NONE: no link"

        # 動詞のチャンクにつながっているチャンクを得る
        subject_chunk = chunks[verb_tok.chunk.link]
        subject_toks = self.get_toks_by_chunk(tree, subject_chunk)  # トークン列を得る
        if not len(subject_toks):  # トークン列が空
            return "NONE: no tokens in linked chunk"

        # トークン列から名詞のトークンを得る
        subject_tok = self.find_pos(subject_toks,"名詞")
        if not subject_tok:  # 見つからなかった
            return "NONE: no noun in linked token list"

        verb_surface = verb_tok.surface  # 動詞の表層形

        return verb_surface

    def cabochaTester(self,sentence):
        cp = CaboCha.Parser()  # パーサー
        tree = cp.parse(sentence)  # 構文木を構築

        # チャンクの辞書を作成
        chunks = self.gen_chunks(tree)

        for chunk in chunks.values():
            r = self.analyze_verb_pronoun_relation(tree, chunks, chunk)
            if r:
                print(r)



if __name__ == "__main__":
    p = MessageParser("エアコンつけて！！")

    # print("名詞---")
    # print(p.GetNouns())
    # print("動詞---")
    # print(p.GetVerb())
    # print("---")
    # print(p.GetParse())
    # print(p.GetSentence())

    while(1):
        print(">>", end = " ")
        ip = input()
        print(p.cabochaTester(ip))