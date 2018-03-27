#!/usr/bin/env python3
# coding: utf-8
# File: hmm_cut.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-3-26

class HmmCut:
    '''加载模型'''
    def load_model(self, model_path):
        f = open(model_path, 'r')
        a = f.read()
        word_dict = eval(a)
        f.close()
        return word_dict

    '''verterbi算法求解'''
    def viterbi(self, obs, states, start_p, trans_p, emit_p):  # 维特比算法（一种递归算法）
        # 算法的局限在于训练语料要足够大，需要给每个词一个发射概率,.get(obs[0], 0)的用法是如果dict中不存在这个key,则返回0值
        V = [{}]
        path = {}
        for y in states:
            V[0][y] = start_p[y] * emit_p[y].get(obs[0], 0)  # 在位置0，以y状态为末尾的状态序列的最大概率
            path[y] = [y]

        for t in range(1, len(obs)):
            V.append({})
            newpath = {}
            for y in states:
                state_path = ([(V[t - 1][y0] * trans_p[y0].get(y, 0) * emit_p[y].get(obs[t], 0), y0) for y0 in states if
                               V[t - 1][y0] > 0])
                (prob, state) = max(state_path)
                V[t][y] = prob
                newpath[y] = path[state] + [y]

            path = newpath  # 记录状态序列
        (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])  # 在最后一个位置，以y状态为末尾的状态序列的最大概率
        return (prob, path[state])  # 返回概率和状态序列

    # 分词主控函数
    def cut(self, sent, trans_path, emit_path, start_path):
        prob_trans = self.load_model(trans_path)
        prob_emit = self.load_model(emit_path)
        prob_start = self.load_model(start_path)
        prob, pos_list = self.viterbi(sent, ('B', 'M', 'E', 'S'), prob_start, prob_trans, prob_emit)
        seglist = list()
        word = list()
        for index in range(len(pos_list)):
            if pos_list[index] == 'S':
                word.append(sent[index])
                seglist.append(word)
                word = []
            elif pos_list[index] in ['B', 'M']:
                word.append(sent[index])
            elif pos_list[index] == 'E':
                word.append(sent[index])
                seglist.append(word)
                word = []
        seglist = [''.join(tmp) for tmp in seglist]
        return prob, seglist


if __name__ == "__main__":

    sent = '维特比算法viterbi的简单实现 python版'
    sent = '''目前在自然语言处理技术中，中文处理技术比西文处理技术要落后很大一段距离，许多西文的处理方法中文不能直接采用，就是因为中文必需有分词这道工序。中文分词是其他中文信息处理的基础，搜索引擎只是中文分词的一个应用。'''
    sent = '北京大学学生前来应聘'
    sent = '新华网驻东京记者报道'
    sent = '我们在野生动物园玩'
   # sent = '2018年12月23日，而我们用到的分词算法是基于字符串的分词方法中的正向最大匹配算法和逆向最大匹配算法。然后对两个方向匹配得出的序列结果中不同的部分运用Bi-gram计算得出较大概率的部分。最后拼接得到最佳词序列。'
    trans_path = './model/prob_trans.model'
    emit_path = './model/prob_emit.model'
    start_path = './model/prob_start.model'
    cuter = HmmCut()
    prob, seglist = cuter.cut(sent, trans_path, emit_path, start_path)
    print(prob)
    print(seglist)

