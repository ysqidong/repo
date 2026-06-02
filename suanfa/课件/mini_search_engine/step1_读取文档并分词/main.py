# 第一步：读取文档并分词

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
    word_list: list[str] = []   # 结果列表
    i = 0   # 当前处理到的字符位置
    wen_zhang_len = len(wen_zhang)  # 文章总长度

    while i < wen_zhang_len:
        wen_zhang_word = wen_zhang[i]

        # 跳过空白字符（空格、换行、制表符）
        if wen_zhang_word.isspace():
            i = i + 1
            continue

        # 跳过标点符号
        # 此功能能覆盖跳过空白字符串功能
        if not wen_zhang_word.isalnum():
            i = i + 1
            continue

        # 尝试匹配词表中的最长词
        # 最大前向匹配
        pi_pei_status = False
        for word in ci_biao:
            word_len = len(word)
            # 检查从当前位置开始、长度为 word_len 的子串是否等于这个词
            if i + word_len <= wen_zhang_len and wen_zhang[i:i + word_len] == word:
                word_list.append(word)
                i = i + word_len
                pi_pei_status = True
                break
        
        # ↑ 此处试用遍历，很慢，如何优化？

        # 如果匹配到了词，进入下一循环
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
            # 没有匹配到此表的单个汉字
            word_list.append(wen_zhang_word)
            i = i + 1

    return word_list


if __name__ == "__main__":
    # 获取当前这个 main.py 文件所在的目录
    dang_qian_mu_lu = os.path.dirname(os.path.abspath(__file__))

    # data 目录在当前目录的上一级，也就是 "12_mini_search_engine/data/"
    # 我们用 os.path.join 来拼接路径，这样在不同操作系统上都能正常工作
    data_mu_lu = os.path.join(dang_qian_mu_lu, "..", "data")

    # 打印一下我们要读取的目录路径
    print("===== 第一步：读取文档并分词 =====")
    print("要读取的目录是：", data_mu_lu)
    print()

    # 用 os.listdir 读取目录里的所有文件和子目录
    all_files = os.listdir(data_mu_lu)

    # 遍历每一个文件
    for file_name in all_files:
        # 跳过词表文件，它不是普通文档
        if file_name == "ci_biao.txt":
            continue

        # 我们只处理以 .txt 结尾的文本文件
        if file_name.endswith(".txt"):
            # 拼接出完整的文件路径
            file_path = os.path.join(data_mu_lu, file_name)

            # 打开文件并读取内容
            # "r" 表示只读模式，encoding="utf-8" 表示用 utf-8 编码读取中文
            # 用 with open 打开文件，这样即使读取时出错，文件也会自动关闭
            with open(file_path, "r", encoding="utf-8") as wen_jian:
                content = wen_jian.read()  # 读取全部内容

            # 调用分词函数
            fen_ci_result = fen_ci(content)

            # 打印文件名和分词结果
            print("文件：", file_name)
            print("分词结果：", fen_ci_result)

            # 使用set去重
            different_words = set(fen_ci_result)

            # 打印去重后的词语数量
            print("这篇文章一共有", len(fen_ci_result), "个词（包含重复）")
            print("这篇文章一共有", len(different_words), "个不同的词（去重后）")
            print("-" * 40)
