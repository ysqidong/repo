# 第三步：有序数组与二分查找

import os


# 读取分词词表
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
    和第二步一样，遍历文档并建立词语到文档列表的映射

    - 参数 data_mu_lu：数据目录的路径
    - 返回：一个字典（哈希表），格式是 {词语: [文档名1, 文档名2, ...]}
    """
    # 准备一个空字典，这就是我们的"倒排索引"
    dao_pai_suo_yin: dict[str, list[str]] = {}

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
            # 用 with open 读取文件，这样即使读取时出错，文件也会自动关闭
            with open(file_path, "r", encoding="utf-8") as wen_jian:
                content = wen_jian.read()

            # 对文件内容分词
            word_list = fen_ci(content)

            # 遍历分词结果中的每一个词语
            for word in word_list:
                if word in dao_pai_suo_yin:
                    if file_name not in dao_pai_suo_yin[word]:
                        dao_pai_suo_yin[word].append(file_name)
                else:
                    dao_pai_suo_yin[word] = [file_name]

    # 返回建好的倒排索引
    return dao_pai_suo_yin


def er_fen_find(arr: list[str], target: str) -> int:
    """
    二分查找函数

    - 参数 arr：一个已经排好序的数组
    - 参数 target：我们要找的目标值
    - 返回：如果找到了，返回目标值的索引；如果没找到，返回 -1
    """
    # 左边界从数组的第一个位置开始
    left = 0
    # 右边界从数组的最后一个位置开始
    right = len(arr) - 1

    # 当左边界不超过右边界时，继续查找
    while left <= right:
        # 计算中间位置
        # 用 left + (right - left) // 2 而不是 (left + right) // 2
        # 是为了防止数字太大时溢出
        # 虽然 Python 不太需要担心这个，但其他语言实操时，这是个好习惯
        mid = left + (right - left) // 2

        # 打印当前查找过程
        print("  正在查找... 左边界=", left, ", 右边界=", right, ", 中间位置=", mid, ", 中间值='", arr[mid], "'")

        # 比较中间值和目标值
        if arr[mid] == target:
            # 找到了！返回中间位置的索引
            print("  找到了！位置在", mid)
            return mid
        elif arr[mid] < target:
            # 中间值比目标小，说明目标在右半边
            # 把左边界移到中间位置的右边
            left = mid + 1
            print("  中间值太小了，目标在右半边")
        else:
            # 中间值比目标大，说明目标在左半边
            # 把右边界移到中间位置的左边
            right = mid - 1
            print("  中间值太大了，目标在左半边")

    # 如果循环结束了还没找到，说明数组里没有目标值
    print("  没找到，目标不在数组里")
    return -1


# =================== 主程序开始 ===================
if __name__ == "__main__":
    # 获取当前目录和 data 目录
    dang_qian_mu_lu = os.path.dirname(os.path.abspath(__file__))
    data_mu_lu = os.path.join(dang_qian_mu_lu, "..", "data")

    print("===== 第三步：有序数组与二分查找 =====")
    print()

    # 建立倒排索引
    dao_pai_suo_yin = jian_li_dao_pai_suo_yin(data_mu_lu)
    print("索引建立完成！一共收录了", len(dao_pai_suo_yin), "个不同的词语。")
    print()

    # 把字典的所有 key（所有词）抽出来，变成一个列表
    suo_you_ci: list[str] = []
    for word in dao_pai_suo_yin:
        suo_you_ci.append(word)

    # ↑ 此处如何优化

    # 用 Python 内置的排序
    # sorted() 函数会返回一个新列表，原列表不会被改变
    you_xu_ci = sorted(suo_you_ci)

    print("词语已经排好序了，前 10 个是：", you_xu_ci[:10])
    print()

    # 让用户输入要搜索的词语
    user_input = input("请输入要搜索的词语：")

    # 对用户输入也进行分词，取第一个词去搜索
    fen_ci_result = fen_ci(user_input)
    if len(fen_ci_result) == 0:
        print("输入为空，无法搜索。")
    else:
        sou_suo_ci = fen_ci_result[0]

        # 先用二分查找确认这个词在不在词表里
        print("开始二分查找词语 '", sou_suo_ci, "'：")
        wei_zhi = er_fen_find(you_xu_ci, sou_suo_ci)

        # 根据查找结果做不同处理
        if wei_zhi != -1:
            # 找到了，再去哈希表里取结果
            word = you_xu_ci[wei_zhi]
            result = dao_pai_suo_yin[word]
            print()
            print("找到了！包含 '", sou_suo_ci, "' 的文档有：", result)
        else:
            print()
            print("抱歉，没有找到包含 '", sou_suo_ci, "' 的文档。")
