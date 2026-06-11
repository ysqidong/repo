#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
final_完整项目 / main.py
简易个人搜索引擎的命令行入口
整合了分词、索引、排序、历史记录和 LRU 缓存等功能
"""

import os
from engine.indexer import build_index, search as single_search
from engine.sorted_terms import get_sorted_terms, binary_search
from engine.ranker import rank_results
from engine.history import Stack, Queue
from engine.lru_cache import LRUCache
from engine.tokenizer import tokenize


def main() -> None:
    # 获取 data 目录路径（假设 data 目录在上一级）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data")

    print("=" * 40)
    print("  简易个人搜索引擎 - 完整版")
    print("=" * 40)
    print()

    # 1. 建立倒排索引
    print("[1/4] 正在建立倒排索引...")
    index = build_index(data_dir)
    print("      索引完成，共收录", len(index), "个不同的词语。")
    print()

    # 2. 构建有序词表（供二分查找使用）
    print("[2/4] 正在构建有序词表...")
    sorted_terms = get_sorted_terms(index)
    print("      有序词表构建完成。")
    print()

    # 3. 初始化历史记录和缓存
    print("[3/4] 正在初始化历史记录和缓存...")
    history_stack = Stack()
    history_queue = Queue()
    cache = LRUCache(3)
    print("      初始化完成。")
    print()

    # 4. 进入交互式搜索循环
    print("[4/4] 搜索引擎已就绪！")
    print("-" * 40)
    print("使用说明：")
    print("  - 直接输入词语：进行搜索")
    print("  - 输入多个词（空格分隔）：多关键词搜索")
    print("  - 输入 'h'：查看上一次搜索")
    print("  - 输入 'r'：查看最近 5 次搜索")
    print("  - 输入 'cache'：查看缓存内容")
    print("  - 输入 'q'：退出程序")
    print("-" * 40)
    print()

    while True:
        user_input = input(">>> 请输入：")

        if user_input == "q":
            print("感谢使用，再见！")
            break

        elif user_input == "h":
            last = history_stack.top()
            if last is None:
                print("      暂无搜索历史。")
            else:
                print("      上一次搜索：", last)
                last_words = tokenize(last)
                if len(last_words) == 0:
                    print("      搜索结果： []")
                elif len(last_words) == 1:
                    result = single_search(index, last_words[0])
                    print("      搜索结果：", result)
                else:
                    result = rank_results(index, last_words)
                    print("      搜索结果：", result)
            print()

        elif user_input == "r":
            recent = history_queue.get_all()
            if len(recent) == 0:
                print("      暂无搜索历史。")
            else:
                print("      最近", len(recent), "次搜索记录：")
                for idx, item in enumerate(recent, 1):
                    print("        ", idx, ".", item)
            print()

        elif user_input == "cache":
            print("      当前缓存内容（越靠前越新）：")
            for key, value in cache.cache_list.to_list():
                print("        ", key, "=>", value)
            print()

        else:
            # 对用户输入进行分词
            words = tokenize(user_input)

            if len(words) == 0:
                print("      输入为空，无法搜索。")
                print()
                continue

            # 尝试从缓存获取结果（用原始输入作为缓存 key，更直观）
            cache_key = user_input
            cached = cache.get(cache_key)

            if cached is not None:
                print("      命中缓存！")
                print("      搜索结果：", cached)
            else:
                if len(words) == 1:
                    # 单关键词搜索：先用二分查找确认词是否存在
                    # 这里先用二分查找确认词是否存在，主要是为了教学演示二分查找的用法
                    pos = binary_search(sorted_terms, words[0])
                    if pos != -1:
                        result = single_search(index, words[0])
                    else:
                        result = []
                else:
                    # 多关键词搜索
                    result = rank_results(index, words)

                print("      搜索结果：", result)
                # 写入缓存
                cache.put(cache_key, result)

            # 更新历史记录
            history_stack.push(cache_key)
            history_queue.enqueue(cache_key)
            if history_queue.size() > 5:
                history_queue.dequeue()

            print()


if __name__ == "__main__":
    main()
