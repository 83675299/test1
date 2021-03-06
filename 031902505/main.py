import sys
import pypinyin


class Node(object):
    # value是该节点存的字，fail是指向的节点，next是子字典，word是目前建立的trie树
    def __init__(self, value=None):
        self.value = value
        self.fail = None
        self.next = dict()
        self.word = ''
        self.isend = False

def read_file(file_path):
    # 读入文件
    with open(file_path, encoding='UTF-8') as words:
        words = words.read().split('\n')
    return words

def convert_pinyin(word):
    #汉字转拼音
    for x in pypinyin.pinyin(word, style=pypinyin.NORMAL):  # 把汉字变成拼音
        k = ''.join(x)
    return k



def tree_build(words):

    # 建树
    root = Node()
    for word in words:
        p = root
        first = 0
        for i in range(0, len(word)):
            k = word[i]
            f = False  # 来判断下一个是否是汉字
            if '\u4e00' <= word[i] <= '\u9fff':
                k=convert_pinyin(word[i])
            if i < len(word) - 1 and '\u4e00' <= word[i + 1] <= '\u9fff':  # 找下一个汉字来解决首字母的问题（成功了一部分）
                u=convert_pinyin(word)
                first = u[0]
                f = True
            k = k.lower()
            for j in range(0, len(k)):
                if k[j] in p.next.keys():
                    p = p.next[k[j]]
                    if j == 0 and f is True:
                        p.next[first] = Node(first)
                    if j == 0 and i == len(word) - 1:
                        p.isend = True
                    continue
                else:
                    p.next[k[j]] = Node(k[j])
                p = p.next[k[j]]
                if j == 0 and f is True:  # 还是解决首字母
                    p.next[first] = Node(first)
                if j == 0 and i == len(word) - 1:
                    p.isend = True
        p.word = word
        p.isend = True
    return root


def ac_build(root):
    # 使用fail指向来做AC机
    queue = []
    queue.insert(0, (root, None))
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
    root.fail = root #没有这句的话会报错
    return root


class AC(object):
    def __init__(self, words):
        self.root = tree_build(words)
        self.root = ac_build(self.root)

    def search(self, words, ans):
        ans_file = open(ans, 'w', encoding='UTF-8')
        out1 = []
        out2 = []
        out3 = []
        count = 0
        begin = 0
        j = 0
        for i in range(0, len(words)):
            word = words[i]
            p = self.root
            for j in range(0, len(word)):
                k = word[j]
                if p == self.root:
                    begin = j
                if '\u4e00' <= k <= '\u9fff': # 如果是中文就进入if
                    k=convert_pinyin(k)
                    for t in range(0, len(k)):
                        if k[t] in p.next.keys():
                           p = p.next[k[t]]
                        elif p.isend is True:
                            out1.append(i)
                            out2.append(p.word)
                            out3.append(word[begin:j])
                            p = self.root
                            count += 1
                        else:
                            p = p.fail
                            if k[t] in p.next.keys():
                                p = p.next[k[t]]
                    continue
                elif 'A' <= k <= 'Z':
                    k = k.lower()
                elif 'a' <= k <= 'z':
                    pass
                elif p.isend is True:
                    out1.append(i)
                    out2.append(p.word)
                    out3.append(word[begin:j])
                    p = self.root
                    count += 1
                else:
                    continue

                if p.isend is True:  # 是否结束，因为有很多情况，所以多复制了几次判断
                    out1.append(i)
                    out2.append(p.word)
                    out3.append(word[begin:j])
                    p = self.root
                    count += 1
                elif k in p.next.keys():  # 进入下个结点
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
                out3.append(word[begin:j + 1])
                count += 1
        write_file(ans_file,count,out1,out2,out3)

def write_file(file,count,out1,out2,out3):
    #输出文件，count是检测出来敏感词的个数
    file.write(f"Total : {count}")
    for i in range(0, count):
        file.write('\n' + f"Line{out1[i] + 1}: <{out2[i]}> {out3[i]}")

if __name__ == '__main__':
    #读命令行的命令
    words = sys.argv[1]
    org = sys.argv[2]
    ans = sys.argv[3]
    ac = AC(read_file(words))
    ac.search(read_file(org),ans)
