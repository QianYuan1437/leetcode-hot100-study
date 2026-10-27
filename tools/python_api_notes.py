"""Extract concise explanations for Python APIs used by a solution snippet."""
from __future__ import annotations

import ast
import builtins


FUNCTION_NOTES = {
    "abs": "abs(x)：返回 x 的绝对值。",
    "all": "all(iterable)：仅当可迭代对象中的所有元素都为真时返回 True；遇到假值会提前停止。",
    "any": "any(iterable)：只要可迭代对象中存在真值就返回 True；命中后会提前停止。",
    "bisect_left": "bisect_left(a, x)：在有序序列中二分查找第一个大于等于 x 的插入位置。",
    "bool": "bool(x)：按 Python 真值规则把对象转换为 True 或 False。",
    "chr": "chr(code)：把 Unicode 码点转换成对应字符。",
    "Counter": "collections.Counter(iterable)：统计各元素出现次数，结果行为类似“元素 → 频次”的字典。",
    "count": "itertools.count()：生成不断递增的惰性计数器，常用于提供唯一序号。",
    "defaultdict": "collections.defaultdict(factory)：访问缺失键时自动用 factory 创建默认值。",
    "deque": "collections.deque(iterable)：双端队列，可在两端以 O(1) 复杂度追加或弹出。",
    "dict": "dict(...)：创建字典，以哈希表保存键值映射，平均查找和写入为 O(1)。",
    "divmod": "divmod(a, b)：一次返回 (a // b, a % b)，适合同时计算进位和当前位。",
    "enumerate": "enumerate(iterable)：遍历元素时同时产生从 0 开始的下标和值。",
    "float": "float(x)：把数值或字符串转换为浮点数。",
    "int": "int(x)：把数值或字符串转换为整数；对浮点数会向 0 截断。",
    "iter": "iter(obj)：取得可迭代对象的迭代器。",
    "len": "len(obj)：返回序列、集合或映射包含的元素数量。",
    "list": "list(iterable)：把可迭代对象收集为列表，或创建空列表。",
    "ListNode": "ListNode(...)：力扣为链表题预先提供的节点类型，通常包含 val 与 next 字段。",
    "max": "max(...)：返回参数或可迭代对象中的最大值。",
    "min": "min(...)：返回参数或可迭代对象中的最小值。",
    "next": "next(iterator)：取得迭代器的下一个元素并推进迭代位置。",
    "Node": "Node(...)：题目或当前代码定义的节点辅助类型，并非 Python 内置类型。",
    "ord": "ord(ch)：返回单个字符的 Unicode 码点，可用于字符与整数下标之间的转换。",
    "range": "range(start, stop, step)：生成按指定步长变化的惰性整数序列，stop 不包含在内。",
    "reversed": "reversed(sequence)：返回反向迭代器，不会原地修改原序列。",
    "set": "set(iterable)：创建去重集合，成员查询平均为 O(1)。",
    "sorted": "sorted(iterable)：返回新的升序列表，不修改原对象。",
    "sum": "sum(iterable)：从左到右累加可迭代对象中的数值。",
    "TreeNode": "TreeNode(...)：力扣为二叉树题预先提供的节点类型，通常包含 val、left 与 right 字段。",
    "TrieNode": "TrieNode()：当前代码定义的前缀树节点类型，并非 Python 内置类型。",
    "tuple": "tuple(iterable)：创建不可变元组；元组可在元素均可哈希时作为字典键。",
    "zip": "zip(*iterables)：按位置并行组合多个可迭代对象，产生元组序列。",
    "heapq.heapify": "heapq.heapify(list)：在线性时间内把列表原地调整为小根堆。",
    "heapq.heappop": "heapq.heappop(heap)：弹出并返回小根堆中的最小元素，同时保持堆性质。",
    "heapq.heappush": "heapq.heappush(heap, item)：把元素压入小根堆并保持堆性质，复杂度 O(log n)。",
}


METHOD_NOTES = {
    "add": "set.add(x)：把 x 加入集合；若已存在则集合保持不变。",
    "append": "list.append(x)：把一个元素追加到列表末尾，均摊复杂度 O(1)。",
    "appendleft": "deque.appendleft(x)：在双端队列左端追加元素，复杂度 O(1)。",
    "copy": "容器的 copy()：创建当前容器的浅拷贝，常用于保存回溯路径快照。",
    "discard": "set.discard(x)：从集合删除 x；x 不存在时不会报错。",
    "extend": "list.extend(iterable)：把可迭代对象中的所有元素依次追加到列表末尾。",
    "get": "dict.get(key, default)：读取键对应的值；键不存在时返回 default 而不是抛出异常。",
    "isdigit": "str.isdigit()：判断字符串是否全部由数字字符组成。",
    "items": "dict.items()：返回字典的“键、值”动态视图，便于成对遍历。",
    "join": "separator.join(strings)：用分隔符连接字符串序列，返回一个新字符串。",
    "keys": "dict.keys()：返回字典所有键的动态视图。",
    "pop": "容器的 pop(...)：删除并返回一个元素；列表默认弹出末尾，字典按键删除。",
    "popleft": "deque.popleft()：删除并返回双端队列最左端元素，复杂度 O(1)。",
    "remove": "容器的 remove(x)：删除指定元素；不存在时通常会抛出异常。",
    "reverse": "list.reverse()：原地反转列表，返回值为 None。",
    "setdefault": "dict.setdefault(key, default)：键存在时返回原值；不存在时写入并返回 default。",
    "sort": "list.sort()：原地排序列表，默认升序，返回值为 None。",
    "values": "dict.values()：返回字典所有值的动态视图。",
}


FIXED_TYPE_METHODS = {
    name
    for fixed_type in (list, dict, set, str, tuple)
    for name in dir(fixed_type)
    if not name.startswith("__")
} | {name for name in dir(__import__("collections").deque) if not name.startswith("__")}


def dotted_name(node: ast.AST) -> str | None:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))
    return None


def explain_python_apis(code: str) -> list[dict[str, str]]:
    tree = ast.parse(code)
    notes: list[dict[str, str]] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        label: str | None = None
        note: str | None = None
        if isinstance(node.func, ast.Name):
            label = node.func.id
            note = FUNCTION_NOTES.get(label)
        elif isinstance(node.func, ast.Attribute):
            dotted = dotted_name(node.func)
            if dotted in FUNCTION_NOTES:
                label, note = dotted, FUNCTION_NOTES[dotted]
            elif node.func.attr in METHOD_NOTES:
                label, note = f".{node.func.attr}()", METHOD_NOTES[node.func.attr]
        if note and label and label not in seen:
            seen.add(label)
            notes.append({"name": label, "description": note})
    return notes


def unexplained_python_api_calls(code: str) -> list[str]:
    """Return built-in/standard/fixed-container calls missing documentation."""
    tree = ast.parse(code)
    imported_names: set[str] = set()
    imported_modules: set[str] = set()
    defined_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined_names.add(node.name)
        elif isinstance(node, ast.Import):
            imported_modules.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported_names.update(alias.asname or alias.name for alias in node.names)

    missing: set[str] = set()
    builtin_names = set(dir(builtins))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            name = node.func.id
            is_python_api = name in builtin_names or name in imported_names
            if is_python_api and name not in FUNCTION_NOTES and name not in defined_names:
                missing.add(name)
        elif isinstance(node.func, ast.Attribute):
            dotted = dotted_name(node.func)
            root = dotted.split(".", 1)[0] if dotted else ""
            if root in imported_modules and dotted not in FUNCTION_NOTES:
                missing.add(dotted or node.func.attr)
            elif node.func.attr in FIXED_TYPE_METHODS and node.func.attr not in METHOD_NOTES:
                missing.add(f".{node.func.attr}()")
    return sorted(missing)

