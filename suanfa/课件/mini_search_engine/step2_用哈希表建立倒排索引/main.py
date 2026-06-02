# 第二步：用哈希表建立倒排索引

import os


# 读取分词词表
# 词表文件在 data 目录下，每行一个词，按长度从长到短排列
dang_qian_mu_lu = os.path.dirname(os.path.abspath(__file__))
ci_biao_lu_jing = os.path.join(dang_qian_mu_lu, "..", "data", "ci_biao.txt")
ci_biao: list[str] = []
with open(ci_biao_lu_jing, "r", encoding="utf-8") as f:
    for line in f:
        ci = line.strip()  # 去掉行首行尾的空白和换行符
        if ci and not ci.startswith("#"):  # 忽略空行和注释行
            ci_biao.append(ci)


def fen_ci(wen_zhang: str) -> list[str]:
    """
    分词函数：基于预定义词表的最大前向匹配分词

    - 参数 wen_zhang：一篇完整的文章（字符串）
    - 返回：一个列表（数组），里面装着拆出来的词语
    """
    word_list: list[str] = []          # 结果列表
    i = 0                     # 当前处理到的字符位置
    wen_zhang_len = len(wen_zhang)        # 文章总长度

    while i < wen_zhang_len:
        wen_zhang_word = wen_zhang[i]

        # 跳过空白字符（空格、换行、制表符）
        if wen_zhang_word.isspace():
            i = i + 1
            continue

        # 跳过标点符号
        if not wen_zhang_word.isalnum():
            i = i + 1
            continue

        # 尝试匹配词表中的最长词（最大前向匹配）
        pi_pei_status = False
        for word in ci_biao:
            word_len = len(word)
            # 检查从当前位置开始、长度为 word_len 的子串是否等于这个词
            if i + word_len <= wen_zhang_len and wen_zhang[i:i + word_len] == word:
                word_list.append(word)
                i = i + word_len
                pi_pei_status = True
                break

        if pi_pei_status:
            continue

        # 如果没有匹配到词表，处理英文/数字连续串
        if ('a' <= wen_zhang_word <= 'z') or ('A' <= wen_zhang_word <= 'Z') or ('0' <= wen_zhang_word <= '9'):
            temp_word: str = ""
            while i < wen_zhang_len:
                char = wen_zhang[i]
                if ('a' <= char <= 'z') or ('A' <= char <= 'Z') or ('0' <= char <= '9'):
                    temp_word = temp_word + char
                    i = i + 1
                else:
                    break
            word_list.append(temp_word)
        else:
            # 没有匹配到词表的单个汉字
            word_list.append(wen_zhang_word)
            i = i + 1

    return word_list


def jian_li_dao_pai_suo_yin(data_mu_lu: str) -> dict[str, list[str]]:
    """
    建立倒排索引函数
    用 Python 字典（哈希表）存储每个词语对应的出现过的文档列表

    - 参数 data_mu_lu：数据目录的路径
    - 返回：一个字典（哈希表），格式是 {词语: [文档名1, 文档名2, ...]}
    """

    # 准备一个空字典，这就是我们的"倒排索引"
    # 每个词对应出现过这个词的文档列表
    dao_pai_suo_yin: dict[str, list[str]] = {}

    # 正排索引：文档出现过哪些词
    # 倒排索引：词出现在哪些文档里
    

    # 读取目录里的所有文件
    all_files = os.listdir(data_mu_lu)

    # 遍历每个文件
    for file_name in all_files:
        # 跳过词表文件，它不是普通文档
        if file_name == "ci_biao.txt":
            continue
        # 只处理 .txt 文件
        if file_name.endswith(".txt"):
            # 拼接完整路径
            file_path = os.path.join(data_mu_lu, file_name)
            # 跳过同名文件夹的情况
            if not os.path.isfile(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as wen_jian:
                content = wen_jian.read()

            # 对文件内容分词
            word_list = fen_ci(content)

            # 遍历分词结果中的每一个词语
            for word in word_list:
                # 如果这个词语已经在字典里了
                if word in dao_pai_suo_yin:
                    # 获取它对应的文档列表
                    doc_list = dao_pai_suo_yin[word]
                    # 如果当前文档还没有被记录，就加进去
                    if file_name not in doc_list:
                        doc_list.append(file_name)
                else:
                    # 如果这个词语还没在字典里，新建一个列表
                    dao_pai_suo_yin[word] = [file_name]

    # 返回建好的倒排索引
    return dao_pai_suo_yin


def search(dao_pai_suo_yin: dict[str, list[str]], word: str) -> list[str]:
    """
    搜索函数：输入一个词，返回包含该词的所有文档
    直接用字典 key 查找，这就是哈希表的优势：速度快

    - 参数 dao_pai_suo_yin：倒排索引（字典）
    - 参数 word：用户要搜索的词
    - 返回：文档列表，如果没有找到就返回空列表
    """
    # 直接用字典的 key 查找，这就是哈希表的优势：速度快
    if word in dao_pai_suo_yin:
        return dao_pai_suo_yin[word]
    else:
        return []


# =================== 主程序开始 ===================
if __name__ == "__main__":
    # 获取当前文件所在目录
    dang_qian_mu_lu = os.path.dirname(os.path.abspath(__file__))

    # 找到 data 目录
    data_mu_lu = os.path.join(dang_qian_mu_lu, "..", "data")

    print("===== 第二步：用哈希表建立倒排索引 =====")
    print("正在读取文档并建立索引...")
    print()

    # 调用函数建立倒排索引
    dao_pai_suo_yin = jian_li_dao_pai_suo_yin(data_mu_lu)

    # 打印一下索引里有多少个不同的词语
    print("索引建立完成！一共收录了", len(dao_pai_suo_yin), "个不同的词语。")
    print()

    # 让用户输入一个词进行搜索
    user_input = input("请输入要搜索的词语：")

    # 对用户输入也进行分词，取第一个词去搜索
    fen_ci_result = fen_ci(user_input)
    if len(fen_ci_result) == 0:
        print("输入为空，无法搜索。")
    else:
        sou_suo_ci = fen_ci_result[0]

        # 调用搜索函数
        result = search(dao_pai_suo_yin, sou_suo_ci)

        # 打印搜索结果
        if len(result) > 0:
            print("找到了！包含 '", sou_suo_ci, "' 的文档有：", result)
        else:
            print("抱歉，没有找到包含 '", sou_suo_ci, "' 的文档。")
