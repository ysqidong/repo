"""
索引模块 (indexer.py)
功能：基于哈希表（Python dict）建立倒排索引
倒排索引是搜索引擎的核心数据结构，格式是：{词语: [包含它的文档列表]}
"""

import os  # 导入 os 模块，用来读取目录和文件
from .tokenizer import tokenize  # 从当前包的 tokenizer 模块导入分词函数


def build_index(data_dir: str) -> dict[str, list[str]]:
    """
    建立倒排索引
    遍历 data 目录下的所有文档，建立词语到文档列表的映射

    - 参数 data_dir：数据目录路径（字符串），里面放着要搜索的文档
    - 返回：倒排索引字典，格式是 {word: [doc_name1, doc_name2, ...]}
    """
    # 准备一个空字典，这就是我们的"倒排索引"
    # 字典是 Python 里的哈希表，查找速度非常快
    index: dict[str, list[str]] = {}

    # 读取目录里的所有文件和子目录名
    all_files = os.listdir(data_dir)

    # 遍历目录里的每一个文件
    for file_name in all_files:
        # 跳过词表文件，它不是普通文档
        if file_name == "ci_biao.txt":
            continue
        # 只处理以 .txt 结尾的文本文件
        if file_name.endswith(".txt"):
            # 用 os.path.join 拼接出完整的文件路径
            # 这样可以兼容 Windows 和 macOS/Linux 的路径格式
            file_path = os.path.join(data_dir, file_name)
            # 跳过同名文件夹的情况
            if not os.path.isfile(file_path):
                continue

            # 打开文件并读取内容
            # "r" 表示只读模式，encoding="utf-8" 确保中文能正常读取
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 对文件内容进行分词
            words = tokenize(content)

            # 遍历分词结果中的每一个词语
            for word in words:
                # 如果这个词语已经在索引字典里了
                if word in index:
                    # 检查当前文档是否已经被记录过
                    if file_name not in index[word]:
                        # 如果没有，就把当前文档名加进去
                        index[word].append(file_name)
                else:
                    # 如果这个词语还没在字典里，新建一个列表，并把当前文档放进去
                    index[word] = [file_name]

    # 返回建好的倒排索引
    return index


def search(index: dict[str, list[str]], word: str) -> list[str]:
    """
    单关键词搜索
    直接用字典 key 查找，这就是哈希表的优势：速度快

    - 参数 index：倒排索引（字典）
    - 参数 word：用户要搜索的词（字符串）
    - 返回：包含该词的文档列表，如果没有找到就返回空列表
    """
    # 直接用字典的 key 查找，这就是哈希表的优势：速度快
    if word in index:
        return index[word]
    return []
