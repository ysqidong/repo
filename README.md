# 北航课程笔记与作业仓库

> 学号 24375352 | 王子昂 | 2024–2025

两门课的代码、作业、课件整理。

---

## 📂 目录结构

```
repo/
├── algorithms/          # 数据结构与算法
│   ├── assignments/     # 8 次作业（data_structure_1~8）
│   ├── code/            # 课堂代码练习
│   ├── notes/           # 手写笔记
│   ├── data/            # 课件文本资料（25 个专题）
│   └── courseware/      # 课件（HTML / Jupyter）
│
├── linux/               # Linux 系统与网络
│   ├── notes/           # Shell / 网络 / Docker 笔记
│   └── route_test/      # FastAPI 路由练习
│
└── .gitignore           # 排除密钥、缓存、IDE 文件
```

---

## 🧠 数据结构与算法

### 作业（`algorithms/assignments/`）

| 文件 | 内容 | 涉及知识点 |
|------|------|-----------|
| `data_structure_1.py` | DeleteItem（手动前移） | 列表、按下标删除 |
| `data_structure_2.py` | SimpleSet 集合类 | 插入 / 查找 / 删除 |
| `data_structure_3.py` | Multipledict 哈希表 | 链地址法、O(1) 查找 |
| `data_structure_4.py` | 优化快速排序 | 随机轴 + 三路分治 |
| `data_structure_5.py` | 单链表实现 | 节点插入 / 删除 / 遍历 |
| `data_structure_6.py` | 链表反转 + 环检测 | 快慢指针、原地反转 |
| `data_structure_7.py` | 二叉树层序遍历 | BFS、队列 |
| `data_structure_8.py` | BST 删除策略 | 前驱 / 后继替换 |
| `4.23作业/` | 链表专项（截图） | 补充材料 |
| `5.29作业.md` | BST 笔记 | 二叉搜索树要点 |

### 代码练习（`algorithms/code/`）

| 文件 | 内容 |
|------|------|
| `stack.py` | 栈的实现（列表底层） |
| `双端队列.py` | collections.deque |
| `链表删除.py` | 单向链表节点删除 |
| `bbble.py` | 冒泡排序 |
| `6.5.py` | MedianFinder（堆） |
| `1.py` | 泛型删除操作 |

### 课件覆盖（`algorithms/data/`）

25 个专题文本：Python 基础 → 排序（冒泡/选择/插入/快排）→ 递归 → 栈/队列 → 哈希 → 列表 → 数组 → 树（二叉树/BST/AVL/堆）→ 图 → 复杂度分析 → 分词/索引/缓存 → 数据库 → Web。

---

## 🐧 Linux 系统

### 笔记（`linux/notes/`）

| 文件 | 内容 |
|------|------|
| `笔记.txt` | Shell 基础 |
| `网络基础笔记.txt` | DNS、网络协议 |
| `docker.md` | Docker 概念与操作 |

### 路由练习（`linux/route_test/`）

`main.py` — FastAPI 路由实践：GET、路径参数、查询参数、POST（Pydantic）、PUT、DELETE、状态码控制、参数验证。

---

## 🛠 运行环境

- Python 3.10+
- 算法作业：纯标准库
- Linux 路由练习：`pip install fastapi "uvicorn[standard]"`
