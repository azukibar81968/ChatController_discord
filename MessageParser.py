# -*- coding: utf-8 -*-

import sys
import MeCab
import CaboCha

SEP_CHAR = '\t'
DICT = ''
WORD_CLASS = 4


class MessageParser:

    def __init__(self, sentence):
        self.Parser = CabochaWrapper(sentence)

    def GetNouns(self):
        """
        名詞の一覧を得る
        """
        return self.Parser.get_nouns()

    def GetVerb(self):
        """
        動詞の一覧を得る
        """
        return self.Parser.get_verbs()

    def GetSymbol(self):
        """
        記号(?とか)の一覧を得る
        """
        return self.Parser.get_symbols()

    def GetSentence(self):
        """
        元の文を得る
        """
        return self.Parser.get_raw_sentence()

    def GetRelatedObject(self):
        """
        verbの目的語を得る
        """
        result = {}
        verbs = self.Parser.get_verbs_toks()
        for i in verbs:
            objects = self.Parser.get_verb_object_pair(i)
            if i.surface in result:
                result[i.surface].append(objects)
            else:
                result[i.surface] = objects


        return result

    def GetTurgetVerb(self, turget):
        """
        turgetと一致する語を含むChunkがかかっている動詞句を得る
        """
        resultList = self.Parser.get_verb_by_obj(turget)
        return resultList

    def IsContainTurget(self,turget):
        resultList = self.Parser.find_turget(turget)
        if len(resultList) == 0:
            return False
        else:
            return True            

    def GetNumDataList(self):
        result = []
        numDataList = self.Parser.get_num_data()
        for i in numDataList:
            classifier_surf = i[1].surface
            try:
                num_surf = int(i[0].surface)
            except:
                continue
            result.append((num_surf,classifier_surf))

        return result

##########MeCabラッパー#############


class MecabWeapper:

    def __init__(self, sentence):
        self.sentence = sentence
        self.m = MeCab.Tagger()

    def GetNouns(self):  # 名詞の一覧を得る
        nouns = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                if "名詞" in analizedData[WORD_CLASS]:
                    nouns.append(analizedData[0])

        return nouns

    def GetVerb(self):  # 動詞の一覧を得る
        verb = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            #print("analizedData = " + str(analizedData))
            if len(analizedData) > WORD_CLASS:
                if "動詞" in analizedData[WORD_CLASS]:
                    verb.append(analizedData[0])
        return verb

    def GetNounsData(self):  # 名詞の詳細の一覧を得る
        nouns = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                if "名詞" in analizedData[WORD_CLASS]:
                    nouns.append(analizedData)

        return nouns

    def GetVerbData(self):  # 動詞の詳細の一覧を得る
        verb = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                if "動詞" in analizedData[WORD_CLASS]:
                    verb.append(analizedData)

        return verb

    def GetParse(self):  # パースデータ全体を得る
        parse = []
        for line in self.m.parse(self.sentence).splitlines():
            analizedData = line.split(SEP_CHAR)
            if len(analizedData) > WORD_CLASS:
                parse.append(analizedData)

        return parse

    def GetSentence(self):  # 元の文を返す
        return self.sentence


##########CaBoChaラッパー#############
class CabochaWrapper:

    def __init__(self, sentence):
        self.sentence = sentence
        self.cp = CaboCha.Parser()  # パーサー
        self.tree = self.cp.parse(sentence)  # 構文木を構築
        self.toks = self.get_toks()
        self.chunks = self.gen_chunks()

        return

    def get_toks(self):
        """
        treeからtoken列を作る
        """
        toks = []

        for i in range(self.tree.size()):  # ツリーのサイズだけ回す
            tok = self.tree.token(i)  # トークンを得る
            toks.append(tok)
        return toks       

    def get_nouns(self):
        """
        名詞の表層系の一覧を作る
        """
        toks = []

        for i in range(self.tree.size()):  # ツリーのサイズだけ回す
            tok = self.tree.token(i)  # トークンを得る
            toks.append(tok)

        toks = self.find_pos(toks, "名詞")

        result = []
        for j in toks:
            result.append(j.surface)

        return result

    def get_nouns_tok(self):
        """
        名詞のtokenの一覧を作る
        """
        toks = []

        for i in range(self.tree.size()):  # ツリーのサイズだけ回す
            tok = self.tree.token(i)  # トークンを得る
            toks.append(tok)

        toks = self.find_pos(toks, "名詞")

        result = []
        for j in toks:
            result.append(j)

        return result

    def get_verbs(self):
        """
        動詞の表層系の一覧を得る
        """
        toks = []

        for i in range(self.tree.size()):  # ツリーのサイズだけ回す
            tok = self.tree.token(i)  # トークンを得る
            toks.append(tok)

        toks = self.find_pos(toks, "動詞")

        result = []
        for j in toks:
            result.append(j.surface)

        return result


    def get_verbs_toks(self):
        """
        動詞のtokenの一覧を得る
        """

        toks = []

        for i in range(self.tree.size()):  # ツリーのサイズだけ回す
            tok = self.tree.token(i)  # トークンを得る
            toks.append(tok)

        toks = self.find_pos(toks, "動詞")

        result = []
        for j in toks:
            result.append(j)

        return result

    def get_symbols(self):
        """
        記号の表層系の一覧を得る
        """

        toks = []

        for i in range(self.tree.size()):  # ツリーのサイズだけ回す
            tok = self.tree.token(i)  # トークンを得る
            toks.append(tok)

        toks = self.find_pos(toks, "記号")

        result = []
        for j in toks:
            result.append(j.surface)

        return result

    def get_symbols(self):
        """
        記号のtokenの一覧を得る
        """

        toks = []

        for i in range(self.tree.size()):  # ツリーのサイズだけ回す
            tok = self.tree.token(i)  # トークンを得る
            toks.append(tok)

        toks = self.find_pos(toks, "記号")

        result = []
        for j in toks:
            result.append(j)

        return result

    def get_raw_sentence(self):
        return self.sentence

    def gen_chunks(self):
        """
        構文木treeからチャンクの辞書を生成する
        """
        chunks = {}
        key = 0  # intにしているがこれはChunk.linkの値で辿れるようにしている

        for i in range(self.tree.size()):  # ツリーのサイズだけ回す
            tok = self.tree.token(i)  # トークンを得る
            if tok.chunk:  # トークンがチャンクを持っていたら
                chunks[key] = tok.chunk  # チャンクを辞書に追加する
                key += 1

        return chunks

    def find_pos(self, toks, pos):
        """
        posの品詞を持つトークンを探す
        """
        results = []
        for tok in toks:
            if pos in tok.feature.split(','):
                results.append(tok)

        return results

    def get_surface_from_toks(self, toks):
        """
        トークン列の表層形をまとめる
        """
        surface = ''
        for tok in toks:
            surface += tok.surface
        return surface

    def get_toks_by_chunk(self, chunk):
        """
        チャンクからトークン列を得る
        """
        beg = chunk.token_pos
        end = chunk.token_pos + chunk.token_size
        toks = []

        for i in range(beg, end):
            tok = self.tree.token(i)
            toks.append(tok)

        return toks

    def get_linking_chunks(self, chunk):
        """
        自分にリンクを張っているチャンク列を得る
        """
        result = []

        for i in self.chunks.values():
            if i.link >= 0:
                if self.chunks[i.link].token_pos == chunk.token_pos:
                    result.append(i)
        return result

    def is_object_chunk(self, chunk):
        """
        目的格かチェックする
        """
        toks = self.get_toks_by_chunk(chunk)
        for i in toks:
            if i.surface == "を":
                return True
        return False

    def is_verb_chunk(self, chunk):
        """
        動詞格かチェックする
        """
        toks = self.get_toks_by_chunk(chunk)
        buf = self.find_pos(toks,"動詞")
        if len(buf) != 0:
            return True
        else:
            return False

    def get_verb_object_pair(self, verb_tok):
        """
        動詞と、対応する目的格のペアの一覧を得る
        """
        # verb_tokの所属するChunkを得る
        chunk = verb_tok.chunk

        # 動詞のチャンクにリンクを張っているチャンク列を得る
        linked_chunks = self.get_linking_chunks(chunk)
        if not len(linked_chunks):
            return "NONE: there is no chunks link to verb"

        object_toks = []

        # print("linked_chunk cnt = " + str(len(linked_chunks)))
        for linked_chunk in linked_chunks:
            if not self.is_object_chunk(linked_chunk):
                continue


            toks = self.get_toks_by_chunk(linked_chunk)  # トークン列を得る
            if not len(toks):  # トークン列が空
                continue # "NONE: no tokens in linked chunk"

            # トークン列から名詞のトークンを得る
            buf = self.find_pos(toks, "名詞")
            if not buf:  # 見つからなかった
                print("there is no noun")
                continue
            object_toks += buf

        object_surfaces = []
        for p in object_toks:  # 名詞の表層形
            object_surfaces.append(p.surface)
            
        return object_surfaces

    def get_num_data(self):
        """
        28度や15時などの数字を含むChunkの数値の数詞を取る
        (数,助数詞)のタプル列を返す
        """
        results = []
        for _,chunk in self.chunks.items():  # ツリーのサイズだけ回す
            toks = self.get_toks_by_chunk(chunk)
            numTok = self.find_pos(toks,"数")
            classifierTok = self.find_pos(toks,"助数詞")
            if len(numTok) != 0 and len(classifierTok) != 0:
                results.append((numTok[0], classifierTok[0]))

        return results

    def find_turget(self, turget):
        """
        turgetのsurfaceを持つトークンを探す
        """
        results = []
        for tok in self.toks:
            if turget == tok.surface:
                results.append(tok)

        return results


    def get_verb_by_obj(self,turget):
        """
        目的格からかかる動詞を探す
        """

        ans = []
        turget_toks = self.find_turget(turget)
        for turget_tok in turget_toks:
            if turget_tok.chunk.link == -1:
                return ans
                
            verbChunk = self.chunks[turget_tok.chunk.link] 

            if self.is_verb_chunk(verbChunk) == False:
                print("not verb!!")
                continue
            else:
                ans.append(self.find_pos(self.get_toks_by_chunk(verbChunk),"動詞")[0].surface)

        return ans
        

if __name__ == "__main__":
    p = MessageParser("15時16分にエアコンを28度で焚くようにして！！")

    print(p.Parser.chunks)

    print(p.Parser.tree.toString(CaboCha.FORMAT_XML))

    print("名詞---")
    print(p.GetNouns())
    print("動詞---")
    print(p.GetVerb())

    p = MessageParser("15時16分にエアコンを28度で焚くようにして！！")

    print("---")
    print(p.IsContainTurget("エアコン"))
    print(p.GetTurgetVerb("エアコン"))
    print("数詞：助数詞---")
    print(p.GetNumDataList())

    print(p.Parser.tree.toString(CaboCha.FORMAT_XML))

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
