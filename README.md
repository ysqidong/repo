# 北航课程笔记与作业仓库

> 学号 24375352 | 王子昂 | 2024–2025

两门课 + 一个独立项目的代码、作业、课件整理。

---

## 📂 目录结构

```
repo/
├── algorithms/              # 数据结构与算法
│   ├── assignments/         # 8 次正式作业 + 2 次补充
│   ├── code/                # 课堂代码练习
│   ├── notes/               # 手写笔记
│   ├── data/                # 课件文本资料（25 个专题）
│   └── courseware/          # 课件（HTML / Jupyter / Notion 导出）
│
├── linux/                   # Linux 系统与网络
│   ├── notes/               # Shell / 网络 / Docker 笔记
│   ├── assignments/         # Docker 作业 ×2 + Python 互动游戏
│   └── route_test/          # FastAPI 路由练习
│
├── projects/                # 独立小项目
│   └── icon_recognizer/     # Windows 桌面图标按颜色自动排列
│
└── .gitignore               # 排除密钥、缓存、IDE 文件
```

---

## 🧠 数据结构与算法

### 作业 (`algorithms/assignments/`)

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
| `4.23作业/` | 链表专项（reverse.py + 截图 + 斯大林排序 HTML） | 补充材料 |
| `5.29作业.md` | BST 笔记 | 二叉搜索树要点 |

### 代码练习 (`algorithms/code/`)

| 文件 | 内容 |
|------|------|
| `stack.py` | 栈的实现（列表底层） |
| `双端队列.py` | collections.deque |
| `链表删除.py` | 单向链表节点删除 |
| `bbble.py` | 冒泡排序 |
| `6.5.py` | MedianFinder（堆） |
| `1.py` | 泛型删除操作 |

### 课件覆盖 (`algorithms/data/`)

25 个专题文本：Python 基础 → 排序（冒泡/选择/插入/快排）→ 递归 → 栈/队列 → 哈希 → 列表 → 数组 → 树（二叉树/BST/AVL/堆）→ 图 → 复杂度分析 → 分词/索引/缓存 → 数据库 → Web。

### 课件材料 (`algorithms/courseware/`)

| 文件/目录 | 内容 |
|-----------|------|
| `1-树的定义.html` ~ `7-堆.html` | Notion 导出的树结构课件（HTML） |
| `4.2.ipynb` | Jupyter 练习 |
| `quick_sort.ipynb` | 快排 Jupyter |
| `data-structures/` | 11 个子项目，每个带 `.ipynb` / `main.py` / `README.md` / `pyproject.toml` |
| `mini_search_engine/` | 6 步渐进式搜索引擎项目，从分词到 LRU 缓存，最终合并为完整引擎 |

**排序相关子项目**（`data-structures/` 下的独立专题）：

| 序号 | 目录 | 内容 |
|------|------|------|
| 1 | `1_list_and_set` | 列表、集合、内存模型、插入/删除图解 |
| 2 | `2_ordered_array_and_binary_search` | 有序数组、二分查找、插入图解 |
| 3 | `3_O` | 大 O 复杂度分析 |
| 4 | `4_bubble` | 冒泡排序、全排列图解 |
| 5 | `5_selection` | 选择排序、逐步图解 |
| 6 | `6_insertion_sort` | 插入排序、扑克牌类比 |
| 7 | `7_hash_table` | 哈希表、链地址法、多表图解 |
| 8 | `8_stack_and_queue` | 栈与队列、盘子/队列图解 |
| 9 | `9_recursio` | 递归、汉诺塔图解 |
| 10 | `10_quick_sort` | 快速排序、复杂度对比图 |
| 11 | `11_linked_list` | 链表（Jupyter） |

---

## 🐧 Linux 系统与网络

### 笔记 (`linux/notes/`)

| 文件 | 内容 |
|------|------|
| `笔记.txt` | Shell 基础命令 |
| `网络基础笔记.txt` | DNS、网络协议要点 |
| `docker.md` | Docker 概念与操作 |

### 作业 (`linux/assignments/`)

#### Docker 作业一：Ollama + Qwen 模型容器化 (`docker_hw1/`)

- 将 Ollama 拉取 Qwen 模型并打包为 Docker 镜像
- 产物：`docker-ollama-qwen.tar.gz`
- 附带截图和 README

#### Docker 作业二：侦探小说生成器 (`docker_hw2/`)

- 容器化部署一个文本生成项目
- 产物：`detective-novel-submit.zip`

#### Python 互动游戏：MoodBox 情绪反馈盒子 (`hw_4.21/`)

- 文件：`moodbox.py`（v3.0）
- 终端互动游戏，含非线性情绪系统、成就系统（10 个成就）、时间挑战
- 需管理耐心值和警觉度两个动态变量，按空格互动
- 支持 Vim 兼容模式、自动 UTF-8 检测
- 运行：`python3 moodbox.py`

### 路由练习 (`linux/route_test/`)

`main.py` — FastAPI 路由实践：GET、路径参数、查询参数、POST（Pydantic）、PUT、DELETE、状态码控制、参数验证。

---

## 🧩 独立项目

### Windows 桌面图标颜色排序器 (`projects/icon_recognizer/`)

- 文件：`desktop_icon_color_sort.py`
- **功能**：自动检测 Windows 桌面图标，提取每个图标的平均颜色（RGB→HSV→颜色名），按颜色顺序（红→橙→黄→绿→青→蓝→紫→未知）自动重新排列图标位置。
- **技术栈**：`win32gui`、`win32con`、`ctypes`、Win32 API（`LVM_GETITEMPOSITION`、`LVM_SETITEMPOSITION32`、`ImageList_GetIcon`、`DrawIconEx`、`GetDIBits` 等）
- **限制**：仅 Windows，且需要图标在桌面为 SysListView32 排列模式

---

## 🛠 运行环境

- Python 3.6+（部分项目需 3.10+）
- 算法作业：纯标准库
- Linux 路由练习：`pip install fastapi uvicorn[standard]`
- MoodBox 游戏：纯标准库，终端需支持 UTF-8
- 桌面图标排序器：`pip install pywin32`，仅 Windows

---

## 📋 课程信息

| 课程 | 学期 | 内容 |
|------|------|------|
| 数据结构与算法 | 2025 春 | 排序、树、图、哈希、链表、搜索引擎项目 |
| Linux 系统与网络 | 2025 春 | Shell、Docker、网络基础、FastAPI |
