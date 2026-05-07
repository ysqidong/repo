import os
from collections import defaultdict

def build_engine(vocab_file):
    # 1. 加载词表并去重 
    if not os.path.exists(vocab_file):
        print(f"❌ 找不到词表文件: {vocab_file}")
        return None, 0

    with open(vocab_file, 'r', encoding='utf-8') as f:
        # 使用 set 保证 10 万个词里没有重复项，且查找速度为 O(1)
        vocab = {line.strip() for line in f if line.strip() and not line.startswith('#')}
    
    max_len = max(len(w) for w in vocab) if vocab else 0
    return vocab, max_len

def run_search_system(vocab_file):
    vocab, max_len = build_engine(vocab_file)
    if vocab is None: return

    # 倒排索引：记录 词语 -> {出现的文件名1, 文件名2} 
    inverted_index = defaultdict(set)
    # 文件词数统计：记录 文件名 -> 总词数
    file_word_counts = {}

    # 2. 遍历并读取当前路径所有 .txt 文件
    for file_name in os.listdir('.'):
        if file_name.endswith('.txt') and file_name != vocab_file:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # --- 正向最大匹配分词 ---
            words_in_doc = []
            i = 0
            while i < len(content):
                match = None
                for length in range(max_len, 0, -1):
                    sub = content[i:i+length]
                    if sub in vocab: # 哈希查找 
                        match = sub
                        break
                if match:
                    words_in_doc.append(match)
                    inverted_index[match].add(file_name) # 记录到索引 
                    i += len(match)
                else:
                    char = content[i].strip()
                    if char:
                        words_in_doc.append(char)
                    i += 1
            
            file_word_counts[file_name] = len(words_in_doc)
            print(f"✅ 已处理: {file_name} (词数: {len(words_in_doc)})")

    # 3. 交互式搜索界面
    print("\n" + "="*30)
    print("🚀 搜索引擎构建完毕！")
    print(f"当前索引词量: {len(inverted_index)}")
    print("="*30)

    while True:
        query = input("\n请输入要查询的关键词 (输入 q 退出): ").strip()
        if query.lower() == 'q': break
        
        if query in inverted_index:
            docs = inverted_index[query]
            print(f"🔍 词语 '{query}' 出现在以下 {len(docs)} 个文档中:")
            for d in docs:
                print(f"  - {d} (该文件总词数: {file_word_counts[d]})")
        else:
            print(f"❌ 未找到与 '{query}' 相关的文档。")

# 运行系统
if __name__ == "__main__":
    run_search_system('ci_biao.txt')