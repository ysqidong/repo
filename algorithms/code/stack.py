class Stack:
    """栈的实现，使用列表作为底层数据结构"""

    def __init__(self):
        """初始化栈"""
        self.items = []

    def is_empty(self):
        """检查栈是否为空"""
        return len(self.items) == 0

    def push(self, item):
        """将元素压入栈顶"""
        self.items.append(item)

    def pop(self):
        """弹出栈顶元素"""
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("栈为空，无法弹出")

    def peek(self):
        """查看栈顶元素，不弹出"""
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("栈为空，无法查看")

    def size(self):
        """返回栈的大小"""
        return len(self.items)

maze=[
    "#########",
    "#S......#",
    "#.#####.#",
    "#...#...#",
    "###.#.###",
    "#...#..E#",
    "#########"
    ]
dirs=[(0,1),(0,-1),(1,0),(-1,0)]#右左下上
def find_path(maze):
    """使用栈来寻找迷宫路径"""
    stack = Stack()
    start = None
    end = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'E':
                end = (i, j)
    if not start or not end:
        return None

    stack.push((start, [start]))  # 将起点和路径压入栈
    visited = set()  # 记录访问过的节点

    while not stack.is_empty():
        current, path = stack.pop()
        if current == end:
            return path  # 找到终点，返回路径
        if current in visited:
            continue
        visited.add(current)

        for dir in dirs:
            next_pos = (current[0] + dir[0], current[1] + dir[1])
            if (0 <= next_pos[0] < len(maze) and
                0 <= next_pos[1] < len(maze[0]) and
                maze[next_pos[0]][next_pos[1]] != '#' and
                next_pos not in visited):
                stack.push((next_pos, path + [next_pos]))  # 将下一个位置和更新后的路径压入栈

    return None  # 没有找到路径

# 测试栈
if __name__ == "__main__":
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print("栈顶元素:", stack.peek())  # 输出: 3
    print("弹出:", stack.pop())       # 输出: 3
    print("栈大小:", stack.size())    # 输出: 2

    # 测试迷宫路径查找
    path = find_path(maze)
    if path:
        print("找到路径:", path)
    else:
        print("没有找到路径")
class Quene:
    """队列的实现，使用列表作为底层数据结构"""

    def __init__(self):
        """初始化队列"""
        self.items = []

    def is_empty(self):
        """检查队列是否为空"""
        return len(self.items) == 0

    def enqueue(self, item):
        """将元素加入队列尾部"""
        self.items.append(item)

    def dequeue(self):
        """从队列头部弹出元素"""
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("队列为空，无法弹出")

    def peek(self):
        """查看队列头部元素，不弹出"""
        if not self.is_empty():
            return self.items[0]
        else:
            raise IndexError("队列为空，无法查看")

    def size(self):
        """返回队列的大小"""
        return len(self.items)