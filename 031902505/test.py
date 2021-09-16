import sys
import unittest
from main import Node
from main import tree_build
from main import AC
from main import ac_build
from main import read_file
from main import convert_pinyin
from main import write_file


class MyTestCase(unittest.TestCase):
    def test1(self):  # 汉字转拼音
        x = '汉'
        x = convert_pinyin(x)
        y = 'han'
        self.assertEqual(x, y)

    def test2(self):  # 测试fail指针的功能
        root = tree_build(r'C:\Users\hqk\Desktop\rgzy\words.txt')
        root = ac_build(root)
        p = root
        p = p.fail
        if 'a' in p.next.keys():
            x = True
        else:
            x = False
        self.assertEqual(x, False)

    def test3(self):  # 测试读入文件
        words = read_file(r'C:\Users\hqk\Desktop\rgzy\333.txt')
        self.assertEqual(words, ['333'])

    def test4(self):
        words = ['比赛', '大龙', '上单', '分钟']
        org = ['在今天的比#$%%^赛中 RNG 1:3 LNG 告负，随着本场比，，，赛的落幕，',
               'RNG2021年LPL夏季赛的征程就此结束。']
        ac = AC(words)
        ac.search(org, r'C:\Users\hqk\Desktop\rgzy\answer1.txt')
        f1=read_file(r'C:\Users\hqk\Desktop\rgzy\answer1.txt')
        f2=read_file(r'C:\Users\hqk\Desktop\rgzy\answer2.txt')
        self.assertEqual(f1,f2)
    def test5(self):
        node = Node('软')
        self.assertEqual(node.value, '软')

if __name__ == '__main__':
    unittest.main()