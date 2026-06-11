"""
分词器模块 (tokenizer.py)
功能：基于预定义词表的最大前向匹配分词
这个模块是搜索引擎的"第一步"，负责把一大段文字拆成一个个可以搜索的词语
"""

import os

# 读取分词词表
# 词表文件在 data 目录下，每行一个词，按长度从长到短排列
vocab_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "data", "ci_biao.txt")
vocab: list[str] = []
with open(vocab_path, "r", encoding="utf-8") as f:
    for line in f:
        word = line.strip()  # 去掉行首行尾的空白和换行符
        if word and not word.startswith("#"):  # 忽略空行和注释行
            vocab.append(word)


def tokenize(text: str) -> list[str]:
    """
    分词函数：基于预定义词表的最大前向匹配分词
    这次我们用预定义词表来做最大前向匹配分词

    - 参数 text：原始文本字符串（比如一篇文章的内容）
    - 返回：清理后的词语列表（一个 Python 列表）
    """
    words: list[str] = []          # 结果列表
    i = 0                # 当前处理到的字符位置
    n = len(text)        # 文章总长度

    while i < n:
        char = text[i]

        # 跳过空白字符（空格、换行、制表符）
        if char.isspace():
            i = i + 1
            continue

        # 跳过标点符号
        if not char.isalnum():
            i = i + 1
            continue

        # 尝试匹配词表中的最长词（最大前向匹配）
        matched = False
        for word in vocab:
            length = len(word)
            # 检查从当前位置开始、长度为 length 的子串是否等于这个词
            if i + length <= n and text[i:i + length] == word:
                words.append(word)
                i = i + length
                matched = True
                break

        if matched:
            continue

        # 如果没有匹配到词表，处理英文/数字连续串
        if ('a' <= char <= 'z') or ('A' <= char <= 'Z') or ('0' <= char <= '9'):
            temp_word: str = ""
            while i < n:
                c = text[i]
                if ('a' <= c <= 'z') or ('A' <= c <= 'Z') or ('0' <= c <= '9'):
                    temp_word = temp_word + c
                    i = i + 1
                else:
                    break
            words.append(temp_word)
        else:
            # 单个汉字 fallback
            words.append(char)
            i = i + 1

    return words
