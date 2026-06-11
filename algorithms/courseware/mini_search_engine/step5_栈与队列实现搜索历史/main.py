# 第六步：栈与队列实现搜索历史

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
    这次我们用预定义词表来做最大前向匹配分词

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
    遍历 data 目录下的所有文档，建立词语到文档列表的映射

    - 参数 data_mu_lu：数据目录的路径
    - 返回：一个字典（哈希表），格式是 {词语: [文档名1, 文档名2, ...]}
    """
    dao_pai_suo_yin: dict[str, list[str]] = {}
    all_files = os.listdir(data_mu_lu)

    for file_name in all_files:
        # 跳过词表文件，它不是普通文档
        if file_name == "ci_biao.txt":
            continue
        if file_name.endswith(".txt"):
            file_path = os.path.join(data_mu_lu, file_name)
            # 用 with open 读取文件，这样即使读取时出错，文件也会自动关闭
            with open(file_path, "r", encoding="utf-8") as wen_jian:
                content = wen_jian.read()
            word_list = fen_ci(content)
            for word in word_list:
                if word in dao_pai_suo_yin:
                    if file_name not in dao_pai_suo_yin[word]:
                        dao_pai_suo_yin[word].append(file_name)
                else:
                    dao_pai_suo_yin[word] = [file_name]

    return dao_pai_suo_yin


def search(dao_pai_suo_yin: dict[str, list[str]], word: str) -> list[str]:
    """
    单关键词搜索

    - 参数 dao_pai_suo_yin：倒排索引（字典）
    - 参数 word：用户要搜索的词
    - 返回：文档列表，如果没有找到就返回空列表
    """
    if word in dao_pai_suo_yin:
        return dao_pai_suo_yin[word]
    else:
        return []


class Stack:

    def __init__(self) -> None:
        # 用一个列表来存储栈里的元素
        self.items: list[str] = []

    def push(self, item: str) -> None:
        """
        入栈：把元素放到列表末尾
        """
        self.items.append(item)

    def pop(self) -> str | None:
        """
        出栈：把列表末尾的元素拿出来
        如果栈是空的，返回 None
        """
        if len(self.items) == 0:
            return None
        return self.items.pop()

    def top(self) -> str | None:
        """
        查看栈顶元素，但不出栈
        """
        if len(self.items) == 0:
            return None
        return self.items[-1]

    def size(self) -> int:
        """
        返回栈里有多少个元素
        """
        return len(self.items)


class Queue:

    def __init__(self) -> None:
        # 用一个列表来存储队列里的元素
        self.items: list[str] = []

    def enqueue(self, item: str) -> None:
        """
        入队：把元素放到列表末尾
        """
        self.items.append(item)

    def dequeue(self) -> str | None:
        """
        出队：把列表最前面的元素拿出来
        """
        if len(self.items) == 0:
            return None
        return self.items.pop(0)

    def front(self) -> str | None:
        """
        查看队首元素，但不出队
        """
        if len(self.items) == 0:
            return None
        return self.items[0]

    def size(self) -> int:
        """
        返回队列里有多少个元素
        """
        return len(self.items)

    def get_all(self) -> list[str]:
        """
        返回队列里所有的元素（不出队）
        """
        return self.items[:]


# =================== 主程序开始 ===================
if __name__ == "__main__":
    dang_qian_mu_lu = os.path.dirname(os.path.abspath(__file__))
    data_mu_lu = os.path.join(dang_qian_mu_lu, "..", "data")

    print("===== 第六步：栈与队列实现搜索历史 =====")
    print()

    # 建立索引
    dao_pai_suo_yin = jian_li_dao_pai_suo_yin(data_mu_lu)
    print("索引建立完成！")
    print()

    # 创建一个栈和一个队列，用来记录搜索历史
    history_stack = Stack()      # 栈：用来查看"上一次"搜索
    history_queue = Queue()   # 队列：用来显示"最近"的搜索

    print("欢迎使用简易搜索引擎！")
    print("提示：输入 'h' 查看上一次搜索，输入 'r' 查看最近 5 次搜索，输入 'q' 退出")
    print()

    # 用一个循环不断接收用户输入
    while True:
        # 获取用户输入
        user_input = input("请输入搜索词（或 h/r/q）：")

        # 如果用户输入 q，退出程序
        if user_input == "q":
            print("再见！")
            break

        # 如果用户输入 h，查看上一次搜索（栈顶）
        elif user_input == "h":
            shang_yi_ci = history_stack.top()
            if shang_yi_ci is None:
                print("还没有搜索历史哦。")
            else:
                print("上一次搜索的是：", shang_yi_ci)
                # 顺便把上一次的搜索结果也展示出来
                # 对历史记录分词后搜索
                fen_ci_result = fen_ci(shang_yi_ci)
                sou_suo_ci = fen_ci_result[0] if len(fen_ci_result) > 0 else shang_yi_ci
                result = search(dao_pai_suo_yin, sou_suo_ci)
                print("搜索结果：", result)
            print()

        # 如果用户输入 r，查看最近 5 次搜索（队列内容）
        elif user_input == "r":
            zui_jin = history_queue.get_all()
            if len(zui_jin) == 0:
                print("还没有搜索历史哦。")
            else:
                print("最近", len(zui_jin), "次搜索记录：")
                for i in range(len(zui_jin)):
                    print("  ", i + 1, ". ", zui_jin[i])
            print()

        # 否则就是正常搜索
        else:
            # 执行搜索
            # 对用户输入分词，取第一个词去搜索
            fen_ci_result = fen_ci(user_input)
            sou_suo_ci = fen_ci_result[0] if len(fen_ci_result) > 0 else user_input
            result = search(dao_pai_suo_yin, sou_suo_ci)

            # 把搜索词压入栈（记录"上一次"）
            history_stack.push(sou_suo_ci)

            # 把搜索词加入队列（记录"最近"）
            history_queue.enqueue(sou_suo_ci)

            # 如果队列里的记录超过 5 条，就把最老的那条出队
            if history_queue.size() > 5:
                history_queue.dequeue()

            # 打印搜索结果
            if len(result) > 0:
                print("找到了！包含 '", sou_suo_ci, "' 的文档有：", result)
            else:
                print("抱歉，没有找到包含 '", sou_suo_ci, "' 的文档。")
            print()
