# 第七步：链表实现 LRU 缓存

import os


# =================== 链表部分 ===================
class Node:
    """
    节点类
    """

    def __init__(self, data: tuple[str, list[str]]) -> None:
        # data 数据类型：元组 (key, value)
        self.data = data
        self.next: Node | None = None


class LinkedList:
    """
    单向链表类
    链表有一个头节点 head，顺着 head 可以访问链表里的所有节点
    """

    def __init__(self) -> None:
        # head 是链表的第一个节点，一开始链表是空的，所以 head 为 None
        self.head: Node | None = None
        # size 记录链表里有多少个节点
        self.size = 0

    def insert_at_head(self, data: tuple[str, list[str]]) -> None:
        """
        在链表头部插入一个新节点
        这是链表最常用、最快的插入方式
        """
        # 创建一个新节点
        new_node = Node(data)
        # 让新节点的 next 指向原来的头节点
        new_node.next = self.head
        # 让 head 指向新节点，新节点就变成了头节点
        self.head = new_node
        # 节点数量加 1
        self.size = self.size + 1

    def delete_node(self, target_data: tuple[str, list[str]]) -> None:
        """
        删除链表中 data 等于 target_data 的节点
        """
        # 如果链表是空的，直接返回
        if self.head is None:
            return

        # 如果要删除的是头节点
        if self.head.data == target_data:
            self.head = self.head.next
            self.size = self.size - 1
            return

        # 从头节点开始遍历链表
        current = self.head
        while current.next is not None:
            # 如果下一个节点就是要删除的节点
            if current.next.data == target_data:
                # 让当前节点的 next 跳过下一个节点，直接指向下下个节点
                current.next = current.next.next
                self.size = self.size - 1
                return
            # 否则继续往后走
            current = current.next

    def delete_tail(self) -> None:
        """
        删除链表的尾节点（最后一个节点）
        """
        # 如果链表是空的，直接返回
        if self.head is None:
            return

        # 如果链表只有一个节点
        if self.head.next is None:
            self.head = None
            self.size = self.size - 1
            return

        # 找到倒数第二个节点
        current = self.head
        while current.next.next is not None:
            current = current.next

        # 让倒数第二个节点的 next 变成 None，最后一个节点就被"丢掉"了
        current.next = None
        self.size = self.size - 1

    def find(self, target_key: str) -> list[str] | None:
        """
        在链表中查找 key 等于 target_key 的节点
        返回对应的 value，如果找不到返回 None
        """
        current = self.head
        while current is not None:
            # 我们的 data 是 (key, value) 的元组
            key, value = current.data
            if key == target_key:
                return value
            current = current.next
        return None

    def move_to_head(self, target_key: str) -> None:
        """
        把 key 等于 target_key 的节点移动到链表头部
        """
        # 如果链表为空，直接返回
        if self.head is None:
            return

        # 如果头节点就是要移动的节点，直接返回（已经在头部了）
        if self.head.data[0] == target_key:
            return

        # 从头遍历，找到目标节点的前一个节点 prev
        prev = self.head
        while prev.next is not None:
            if prev.next.data[0] == target_key:
                # 找到目标节点，把它摘出来
                target_node = prev.next
                prev.next = target_node.next
                self.size = self.size - 1
                # 把目标节点插入头部
                target_node.next = self.head
                self.head = target_node
                self.size = self.size + 1
                return
            prev = prev.next

    def to_list(self) -> list[tuple[str, list[str]]]:
        """
        把链表转换成一个 Python 列表，方便打印查看
        """
        result: list[tuple[str, list[str]]] = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result


# =================== LRU 缓存部分 ===================
class LRUCache:
    """
    LRU 缓存类
    LRU = Least Recently Used，最近最少使用
    意思是：当缓存满了的时候，把最久没被访问过的数据淘汰掉
    """

    def __init__(self, capacity: int) -> None:
        # capacity 是缓存的最大容量，我们这里设为 3
        self.capacity = capacity
        # 用链表来保存缓存数据，最近使用的放在头部，最久未使用的放在尾部
        self.cache_list = LinkedList()

    def get(self, key: str) -> list[str] | None:
        """
        获取缓存中的数据
        如果 key 存在，把这个节点移到头部（表示最近使用了），返回 value
        如果 key 不存在，返回 None
        """
        value = self.cache_list.find(key)
        if value is not None:
            # 找到了！把它移到头部，表示最近使用过
            self.cache_list.move_to_head(key)
            return value
        return None

    def put(self, key: str, value: list[str]) -> None:
        """
        向缓存中放入数据
        如果 key 已存在，更新 value 并移到头部
        如果 key 不存在，在头部插入新节点；如果满了，删除尾部节点
        """
        # 先检查 key 是否已经存在
        existing_value = self.cache_list.find(key)
        if existing_value is not None:
            # 已存在，更新并移到头部
            self.cache_list.delete_node((key, existing_value))
            self.cache_list.insert_at_head((key, value))
            return

        # 如果缓存还没满，直接在头部插入
        if self.cache_list.size < self.capacity:
            self.cache_list.insert_at_head((key, value))
        else:
            # 缓存满了，先删除尾部（最久未使用的），再在头部插入新的
            self.cache_list.delete_tail()
            self.cache_list.insert_at_head((key, value))


# =================== 搜索引擎部分 ===================
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
    直接用字典 key 查找，这就是哈希表的优势：速度快

    - 参数 dao_pai_suo_yin：倒排索引（字典）
    - 参数 word：用户要搜索的词
    - 返回：文档列表，如果没有找到就返回空列表
    """
    if word in dao_pai_suo_yin:
        return dao_pai_suo_yin[word]
    else:
        return []


# =================== 主程序开始 ===================
if __name__ == "__main__":
    dang_qian_mu_lu = os.path.dirname(os.path.abspath(__file__))
    data_mu_lu = os.path.join(dang_qian_mu_lu, "..", "data")

    print("===== 第七步：链表实现 LRU 缓存 =====")
    print()

    # 建立索引
    dao_pai_suo_yin = jian_li_dao_pai_suo_yin(data_mu_lu)
    print("索引建立完成！")
    print()

    # 创建一个容量为 3 的 LRU 缓存
    cache = LRUCache(3)

    print("欢迎使用带缓存的搜索引擎！")
    print("提示：输入 'cache' 查看缓存内容，输入 'q' 退出")
    print()

    # 循环接收用户输入
    while True:
        user_input = input("请输入搜索词（或 cache/q）：")

        if user_input == "q":
            print("再见！")
            break

        elif user_input == "cache":
            print("当前缓存内容（越靠前越新）：")
            cache_content = cache.cache_list.to_list()
            for item in cache_content:
                print("  ", item[0], "=>", item[1])
            print()

        else:
            # 对用户输入分词，取第一个词作为缓存 key 和搜索词
            fen_ci_result = fen_ci(user_input)
            if len(fen_ci_result) == 0:
                print("输入为空，无法搜索。")
                print()
                continue
            sou_suo_ci = fen_ci_result[0]

            # 先查缓存
            cache_result = cache.get(sou_suo_ci)

            if cache_result is not None:
                # 缓存命中！
                print("命中缓存！")
                print("搜索结果：", cache_result)
            else:
                # 缓存没命中，去索引里查
                result = search(dao_pai_suo_yin, sou_suo_ci)
                print("搜索结果：", result)
                # 把结果放入缓存
                cache.put(sou_suo_ci, result)

            print()
