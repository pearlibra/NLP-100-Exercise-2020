from http.client import ImproperConnectionState
from itertools import combinations
import re
from knock41 import sentences


for sentence in sentences:
    nouns = []  # 名詞を含むチャンクのインデックス番号
    for i, chunk in enumerate(sentence.chunks):
        if '名詞' in [morph.pos for morph in chunk.morphs]:  # 名詞を含む文節を抽出
            nouns.append(i)  # ある一文のチャンクの中に名詞が含まれたときにそのチャンクのインデックス番号をnounsに追加
    for i, j in combinations(nouns, 2):  # 名詞を含む文節のペアごとにパスを作成
        path_i = []  # 一つ目として与えられた名詞からのパスを格納するリスト．
        path_j = []  # 2つ目として...
        # iから辿っていってjと重なった→len(path_j)は0のはず．途中でiがjを通り越してしまったら次はjから始まるパスを追加していく．ijが重なったら終了．重ならないことは多分ない
        while i != j:
            if i < j:  # 文節番号iから始めるパス
                path_i.append(i)  # 文節番号iの方が早かったらpath_iに入れる
                i = sentence.chunks[i].dst  # 名詞チャンクの係先チャンクインデックスに変える　i
            else:
                path_j.append(j)
                j = sentence.chunks[j].dst
        if len(path_j) == 0:  # 1つ目のケース iからdst辿っていってjと重なったなら，一回もiはjを超えていないはずなのでこの条件が成り立つはず
            chunk_X = ''.join([morph.surface if morph.pos !=
                               '名詞' else 'X' for morph in sentence.chunks[path_i[0]].morphs])  # 始点の名詞が含まれるchunkで，名詞はXに変えてそれ以外はそのまま
            chunk_Y = ''.join([morph.surface if morph.pos !=
                               '名詞' else 'Y' for morph in sentence.chunks[i].morphs])  # ここでiを使ってるのはi=jだから
            chunk_X = re.sub('X+', 'X', chunk_X)  # 連結名詞をXXとかじゃなくXに
            chunk_Y = re.sub('Y+', 'Y', chunk_Y)  # 二つ目の名刺も同様に連結名詞対策
            path_XtoY = [chunk_X] + [''.join(morph.surface for morph in sentence.chunks[n].morphs)
                                     for n in path_i[1:]] + [chunk_Y]
            print(' -> '.join(path_XtoY))
        else:  # 2つ目のケース
            chunk_X = ''.join([morph.surface if morph.pos !=
                               '名詞' else 'X' for morph in sentence.chunks[path_i[0]].morphs])  # １個目の名詞が含まれるチャンク
            chunk_Y = ''.join([morph.surface if morph.pos !=
                               '名詞' else 'Y' for morph in sentence.chunks[path_j[0]].morphs])  # ２個目の名詞が含まれるチャンク
            chunk_k = ''.join(
                [morph.surface for morph in sentence.chunks[i].morphs])  # 二つの名詞からdst辿っていって重なった文節
            chunk_X = re.sub('X+', 'X', chunk_X)  # 連結名詞対策
            chunk_Y = re.sub('Y+', 'Y', chunk_Y)  # 連結名詞対策
            path_X = [
                chunk_X] + [''.join(morph.surface for morph in sentence.chunks[n].morphs) for n in path_i[1:]]  # １個目の名刺からのパス
            path_Y = [
                chunk_Y] + [''.join(morph.surface for morph in sentence.chunks[n].morphs) for n in path_j[1:]]  # 2個目の名詞からのパス
            print(' | '.join(
                [' -> '.join(path_X), ' -> '.join(path_Y), chunk_k]))
