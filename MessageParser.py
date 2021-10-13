# -*- coding: utf-8 -*-

import sys
import MeCab
import CaboCha

SEP_CHAR = '\t'
DICT = ''
WORD_CLASS = 4

class MessageParser:

    def __init__(self, sentence):
        self.Parser = MecabWeapper(sentence)

    def GetNouns(self):
        """
        名詞の一覧を得る
        """
        return self.Parser.GetNouns()

    def GetVerb(self):
        """
        動詞の一覧を得る
        """
        return self.Parser.GetVerb()

    def GetSentence(self):
        return self.Parser.GetSentence()

    def GetRelatedSubject(self,verb):
        return "NO DATA"

    def GetRelatedObject(self,verb):
        return "NO DATA"



##########MeCabラッパー#############


class MecabWeapper:

    def __init__(self, sentence):
        self.sentence = sentence
        self.m = MeCab.Tagger()

    def GetNouns(self):#名詞の一覧を得る
        nouns = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                if "名詞" in analizedData[WORD_CLASS]:
                    nouns.append(analizedData[0])

        return nouns

    def GetVerb(self):#動詞の一覧を得る
        verb = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            #print("analizedData = " + str(analizedData))
            if len(analizedData) > WORD_CLASS:
                if "動詞" in analizedData[WORD_CLASS]:
                    verb.append(analizedData[0])
        return verb

    def GetNounsData(self):#名詞の詳細の一覧を得る
        nouns = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                if "名詞" in analizedData[WORD_CLASS]:
                    nouns.append(analizedData)

        return nouns

    def GetVerbData(self):#動詞の詳細の一覧を得る
        verb = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                if "動詞" in analizedData[WORD_CLASS]:
                    verb.append(analizedData)

        return verb

    def GetParse(self):#パースデータ全体を得る
        parse = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                parse.append(analizedData)

        return parse

    def GetSentence(self):#元の文を返す
        return self.sentence


##########CaBoChaラッパー#############
class CabochaWrapper:

    def __init__(self, sentence):
        self.sentence = sentence
        self.cp = CaboCha.Parser()  # パーサー
        self.tree = self.cp.parse(sentence)  # 構文木を構築
        self.chunks = self.gen_chunks()
        
        return

    def get_raw_sentence(self):
        return self.sentence

    def gen_chunks(self):
        """
        構文木treeからチャンクの辞書を生成する
        """
        chunks = {}
        key = 0  # intにしているがこれはChunk.linkの値で辿れるようにしている

        for i in range(tree.size()):  # ツリーのサイズだけ回す
            tok = self.tree.token(i)  # トークンを得る
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

    def get_linking_chunks(self,chunks, chunk):
        """
        自分にリンクを張っているチャンク列を得る
        """
        result = []

        for i in chunks.values():
            if i.link >= 0:
                if chunks[i.link] == chunk:
                    result.append(i)
        return result

    def analyze_verb_pronoun_relation(self, chunks, chunk):
        # 引数chunkからトークン列を得る
        verb_toks = self.get_toks_by_chunk(self.tree, chunk)
        if not len(verb_toks):
            return "NONE: no token list"

        # トークン列から動詞トークンを探す
        verb_tok = self.find_pos(verb_toks, '動詞')
        if not verb_tok:  # 見つからなかった
            return "NONE: no verb token"
        if not verb_tok.chunk:
            return "NONE: chunk unavailable"


        # 動詞のチャンクにリンクを張っているチャンク列を得る
        subject_chunks = self.get_linking_chunks(chunks, chunk)
        if not len(subject_chunks):
            return "NONE: there is no chunks link to verb"

        for subject_chunk in subject_chunks:
            subject_toks = self.get_toks_by_chunk(self.tree, subject_chunk)  # トークン列を得る
            if not len(subject_toks):  # トークン列が空
                return "NONE: no tokens in linked chunk"

            # トークン列から名詞のトークンを得る
            subject_tok = self.find_pos(subject_toks,"名詞")
            post_positional_perticle_tok = self.find_pos(subject_toks,"助詞")
            if not subject_tok:  # 見つからなかった
                continue
            if post_positional_perticle_tok.surface != "を":
                continue


            subject_surface = subject_tok.surface  # 動詞の表層形

        return subject_surface


if __name__ == "__main__":
    p = MessageParser("エアコンつけて！！")

    print("名詞---")
    print(p.GetNouns())
    print("動詞---")
    print(p.GetVerb())
    print("---")
    # print(p.GetParse())
    print(p.GetSentence())

    # while(1):
    #     print(">>", end = " ")
    #     ip = input()
    #     print(p.cabochaTester(ip))


    # def cabochaTester(self,sentence):
    #     cp = CaboCha.Parser()  # パーサー
    #     tree = cp.parse(sentence)  # 構文木を構築
    #     print(tree.toString(CaboCha.FORMAT_XML))

    #     # チャンクの辞書を作成
    #     chunks = self.gen_chunks(tree)
        
    #     for chunk in chunks.values():
    #         r = self.analyze_verb_pronoun_relation(tree, chunks, chunk)
    #         if r:
    #             toks = self.get_toks_by_chunk(tree,chunk)
    #             print(toks[0].surface + ": " + r)

