import json
import pypinyin


class Node(object):
    # value是该节点存的字，fail是指向的节点，next是子字典，word是目前建立的try树
    def __init__(self, value=None):
        self.value = value
        self.fail = None
        self.next = dict()
        self.word = ''
        self.isend = False


class AC(object):
    def __init__(self, words):
        self.root = AC.ac_build(self, words)

    def ac_build(self, file):
        # 读入文件
        with open(file, encoding='UTF-8') as words:
            words = words.read().split('\n')
        # 建树
        root = Node()
        p = Node()
        for word in words:
            p = root
            length=len(word)
            for i in range(0,len(word)):
                k=word[i]
                f=False#来判断下一个是否是汉字
                if '\u4e00' <= word[i] <= '\u9fff':
                    for x in pypinyin.pinyin(word[i], style=pypinyin.NORMAL):  # 把汉字变成拼音
                        k = ''.join(x)
                if i <len(word)-1 and '\u4e00' <= word[i+1] <= '\u9fff':#找下一个汉字来解决首字母的问题（成功了一部分）
                    for x in pypinyin.pinyin(word[i+1], style=pypinyin.NORMAL):  # 把汉字变成拼音
                        u = ''.join(x)
                        first=u[0]
                        f = True

                for j in range(0, len(k)):
                    if k[j] in p.next.keys():
                        p = p.next[k[j]]
                        if j == 0 and f == True:
                            p.next[first] = Node(first)
                        if j == 0 and i == len(word) - 1:
                            p.isend = True
                        continue
                    else:
                        p.next[k[j]] = Node(k[j])
                    p = p.next[k[j]]
                    if j==0 and f==True:#还是解决首字母
                        p.next[first]=Node(first)
                    if j==0 and i==len(word)-1:
                        p.isend=True
            p.word = word
            p.isend = True
        # 使用fail指向来做AC机
        queue = []
        queue.insert(0, (root, None))
        temp = None
        while len(queue) > 0:
            node_parent = queue.pop()
            temp, parent = node_parent[0], node_parent[1]
            for i in temp.next.values():
                queue.insert(0, (i, temp))
            if parent is None:
                continue
            elif parent is root:
                temp.fail = root
            else:
                fail = parent.fail
                while fail and temp.value not in fail.next:
                    fail = fail.fail
                if fail:
                    temp.fail = fail.next[temp.value]
                else:
                    temp.fail = root
        root.fail = root
        return root

    def search(self, file):
        with open(file, encoding='UTF-8') as words:
            words = words.read().split('\n')
        out1 = []
        out2 = []
        out3 = []
        count = 0
        for i in range(0, len(words)):
            word = words[i]
            p = self.root
            for j in range(0, len(word)):
                ischinese = False
                k = word[j]
                if p == ac.root:
                    begin = j
                if '\u4e00' <= k <= '\u9fff':
                    for x in pypinyin.pinyin(k, style=pypinyin.NORMAL):  # 把汉字拆成拼音，对单个字母检索
                        k = ''.join(x)
                        for l in range(0, len(k)):
                            if k[l] in p.next.keys():
                                p = p.next[k[l]]
                            elif p.isend is True:
                                out1.append(i)
                                out2.append(p.word)
                                out3.append(word[begin:j])
                                p = self.root
                                count += 1
                            else:
                                p = p.fail
                                if k[l] in p.next.keys():
                                    p = p.next[k[l]]
                    continue
                elif 'A' <= k <= 'Z':
                    k = k.lower()
                elif 'a' <= k <= 'z':
                    None
                elif p.isend is True:
                    out1.append(i)
                    out2.append(p.word)
                    out3.append(word[begin:j])
                    p = self.root
                    count += 1
                else:
                    continue

                if p.isend is True:#是否结束，因为有很多情况，所以多复制了几次判断
                    out1.append(i)
                    out2.append(p.word)
                    out3.append(word[begin:j])
                    p = self.root
                    count += 1
                elif k in p.next.keys():#进入下个结点
                    p = p.next[k]
                else:
                    p = p.fail
                    if k in p.next.keys():
                        p = p.next[k]
                    else:
                        p = self.root
            if p.isend is True:
                out1.append(i)
                out2.append(p.word)
                out3.append(word[begin:j+1])
                p = self.root
                count += 1
            p = self.root

        print(f"total : {count}")
        for i in range(0, count):
            print(f"Line{out1[i] + 1}: <{out2[i]}> {out3[i]}")


if __name__ == '__main__':
    ac = AC(r'C:\Users\hqk\Desktop\软工作业\words.txt')
    ac.search(r'C:\Users\hqk\Desktop\软工作业\org.txt')
