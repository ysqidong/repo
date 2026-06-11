# 北航课程笔记与作业仓库

> 学号 24375352 | 王子昂 | 2024–2025

两门课的代码、作业、课件整理。

---

## 📂 目录结构

```
repo/
├── algorithms/          # 数据结构与算法
│   ├── assignments/     # 四次作业
│   ├── code/            # 课堂代码练习
│   ├── notes/           # 手写笔记
│   ├── data/            # 课件文本资料（25 个专题）
│   └── courseware/      # 课件（HTML / Jupyter）
│
├── linux/               # Linux 系统与网络
│   ├── notes/           # Shell / 网络 / Docker 笔记
│   └── route_test/      # FastAPI 路由练习
│
└── .vscode/             # VS Code 配置
```

---

## 🧠 数据结构与算法

### 作业（`algorithms/assignments/`）

| 文件 | 内容 | 涉及知识点 |
|------|------|-----------|
| `第二次作业.py` | 集合类 SimpleSet | 列表、插入/删除/查询 |
| `第三次作业.py` | Multipledict 哈希表 | 哈希、字典、O(1) 查找 |
| `4.9作业.py` | 优化快速排序 | 随机轴选择、分治 |
| `5.29作业.md` | 二叉搜索树 | BST 构建、节点操作 |

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

25 个专题文本：Python 基础 → 排序（冒泡/选择/插入/快排）→ 递归 → 栈/队列 → 哈希 → 列表 → 数组 → 树（二叉树/BST/AVL/堆）→ 图 → 复杂度分析 → 分词/索引/缓存 → 数据库 → Web — 覆盖完整的数据结构课程体系。

---

## 🐧 Linux 系统

### 笔记（`linux/notes/`）

| 文件 | 内容 |
|------|------|
| `笔记.txt` | Shell 基础（Ctrl+C/D、终端操作、Python 集合库引用） |
| `网络基础笔记.txt` | DNS、网络协议基础 |
| `docker.md` | Docker 概念与操作入门 |

### 路由练习（`linux/route_test/`）

`main.py` — FastAPI 完整路由实践，涵盖 8 种路由模式：基础 GET、路径参数、查询参数、POST 请求体（Pydantic 模型）、PUT 更新、DELETE、状态码控制、参数验证。

---

## ⚠️ 安全提示

仓库根目录下 `id_rsa.pub` **不应公开**，建议：

```bash
git rm --cached id_rsa.pub
echo "id_rsa.pub" >> .gitignore
git commit -m "移除公钥文件"
```

虽然公钥本身危害较小，但暴露用户名和机器指纹仍是不好的习惯。

---

## 🛠 运行环境

- Python 3.10+
- 算法作业：纯标准库，无需额外依赖
- Linux 路由练习：`pip install fastapi "uvicorn[standard]"`
