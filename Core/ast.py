"""SLang-Core AST 模块 — 抽象语法树定义、递归下降解析器与求值器。

解析流程
--------
1. parse(text, known_names)  扫描文本，将 【函数名 参数>=<参数...】 结构转换为 AST 节点列表
2. evaluate(nodes, slang)   递归遍历节点列表求值：
   - TextNode      → 原样输出
   - FunctionNode  → 递归求值参数后调用 register.call()
   - 控制流节点    → AST 层直接处理（判断 / 比较- / 循环-）

AST 节点类型
------------
TextNode       纯文本片段（不被 【】 包围的部分）
FunctionNode   函数调用，包含函数名和参数列表
               参数列表中每个元素是一个 list[ASTNode]（一个参数可能含嵌套调用）

已知函数名驱动
--------------
Slang 语法中，函数名和参数之间没有强制分隔符（如【函数名 参数】），
因此解析器必须依赖已知函数名集合来判定函数名边界。
采用最长匹配策略：在当前位置尝试所有已知函数名，取最长匹配。
"""


class ASTNode:
    """AST 节点基类。"""
    pass


class TextNode(ASTNode):
    """纯文本节点——不被 【】 包围的文本片段。"""

    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f'TextNode({self.text!r})'


class FunctionNode(ASTNode):
    """函数调用节点。

    Attributes:
        name:   注册的函数名（如 "调试输出"、"获取变量"）
        params: 参数列表，每个元素为 list[ASTNode]
                - 空列表 [] 表示该参数不存在
                - 包含元素表示参数内容（可含纯文本和嵌套调用）
    """

    def __init__(self, name: str, params: list):
        self.name = name
        self.params = params  # list[list[ASTNode]]

    def __repr__(self):
        return f'FunctionNode({self.name!r}, params={self.params!r})'


# ═══════════════════════════════════════════════════════════════════
# 递归下降解析器
# ═══════════════════════════════════════════════════════════════════

def parse(text: str, known_names: set = None) -> list[ASTNode]:
    """将 Slang 文本解析为 AST 节点列表。

    顶层扫描：
    - 遇到 【 → 进入 _parse_function() 递归解析函数调用
    - 其他字符 → 收集为 TextNode

    Args:
        text: 完整的 Slang 源代码文本
        known_names: 已知函数名集合，用于消歧函数名边界

    Returns:
        顶层 AST 节点列表
    """
    if known_names is None:
        known_names = set()

    nodes = []
    i = 0
    while i < len(text):
        if text[i] == '【':
            node, i = _parse_function(text, i, known_names)
            nodes.append(node)
        else:
            start = i
            while i < len(text) and text[i] != '【':
                i += 1
            if i > start:
                nodes.append(TextNode(text[start:i]))
    return nodes


def _parse_function(text: str, start: int, known_names: set) -> 'tuple[FunctionNode, int]':
    """从 start（指向 '【'）解析一个函数调用。

    由于 Slang 语法中函数名与参数之间没有强制分隔符，
    解析器使用最长匹配策略：在已知函数名中查找从当前位置开始的最长匹配。

    语法:  '【' 函数名 ( '>=<' 参数 )* '】'

    Returns:
        (FunctionNode, 下一个待扫描的字符索引)
    """
    i = start + 1  # 跳过 '【'

    # ── 1. 使用已知函数名集合进行最长匹配 ──
    name = ''
    for candidate in known_names:
        if text.startswith(candidate, i) and len(candidate) > len(name):
            name = candidate

    # 如果没有匹配到已知函数名，则扫描到 '>=<' 或 '】' 作为函数名
    if not name:
        name_end = i
        while name_end < len(text):
            c = text[name_end]
            if c == '】':
                break
            if text[name_end:name_end + 3] == '>=<':
                break
            name_end += 1
        name = text[i:name_end]
    else:
        name_end = i + len(name)

    # ── 2. 无参数分支（函数名后紧跟 '】'）──
    if name_end < len(text) and text[name_end] == '】':
        return FunctionNode(name, []), name_end + 1

    # ── 3. 有参数 ──
    # 找到函数体的结束位置（查找匹配的 '】'）
    # 注意：外层 '【' 已被消费，故 depth 从 1 开始计数
    body_start = name_end
    depth = 1
    body_end = name_end
    while body_end < len(text):
        c = text[body_end]
        if c == '【':
            depth += 1
        elif c == '】':
            depth -= 1
            if depth == 0:
                break
        body_end += 1

    body = text[body_start:body_end]

    # ── 4. 按顶级 '>=<' 切分参数，递归解析各参数 ──
    params_raw = _split_params(body)
    params = [parse(p, known_names) for p in params_raw if p]

    return FunctionNode(name, params), body_end + 1


def _split_params(body: str) -> list[str]:
    """按最外层 '>=<' 分隔符切分参数文本。

    嵌套在 【...】 内的 >=< 不会被当成分隔符。
    """
    parts = []
    current = []
    i = 0
    depth = 0
    while i < len(body):
        if body[i] == '【':
            depth += 1
            current.append(body[i])
            i += 1
        elif body[i] == '】':
            depth -= 1
            current.append(body[i])
            i += 1
        elif body[i:i + 3] == '>=<' and depth == 0:
            parts.append(''.join(current))
            current = []
            i += 3
        else:
            current.append(body[i])
            i += 1
    parts.append(''.join(current))
    # 对每个参数 strip 首尾空白，消除排版缩进
    return [p.strip() for p in parts]


# ═══════════════════════════════════════════════════════════════════
# 求值器
# ═══════════════════════════════════════════════════════════════════

def evaluate(nodes: list[ASTNode], slang) -> str:
    """对 AST 节点列表求值，拼接返回字符串。

    求值规则：
    - TextNode        → 直接输出文本
    - FunctionNode    → 递归求值参数 → 调用注册函数
    - 控制流函数      → AST 层直接处理，不经过 register.call()

    Args:
        nodes: parse() 返回的节点列表
        slang: Slang 实例（提供 register 和 _dict）

    Returns:
        求值结果字符串
    """
    result = []
    for node in nodes:
        if isinstance(node, TextNode):
            result.append(node.text)
        elif isinstance(node, FunctionNode):
            result.append(_eval_function(node, slang))
    return ''.join(result)


def _eval_function(node: FunctionNode, slang) -> str:
    """求值单个函数调用节点。"""
    # 控制流 —— AST 层直接处理
    if node.name in ('判断', '比较-', '循环-'):
        return _eval_control_flow(node, slang)

    # 常规函数 —— 递归求值参数后调用 register
    evaled_params = []
    for param_nodes in node.params:
        evaled_params.append(evaluate(param_nodes, slang))

    ret = slang.register.call(node.name, evaled_params, slang._dict)
    if ret is None:
        return ''
    return str(ret)


def _eval_control_flow(node: FunctionNode, slang) -> str:
    """控制流求值 —— 判断 / 比较- / 循环-。

    这些函数不走 register.call()，因为需要短路求值或循环控制，
    register 中仅通过 reg_not_callable 占位。
    """
    name = node.name

    # ── 判断 ──
    if name == '判断':
        if len(node.params) < 3:
            return ''
        cond = evaluate(node.params[0], slang)
        if cond in ('True', 'true', '真', '1'):
            return evaluate(node.params[1], slang)
        else:
            return evaluate(node.params[2], slang)

    # ── 比较- ──
    if name == '比较-':
        if len(node.params) < 4:
            return ''
        op = evaluate(node.params[0], slang)
        left = evaluate(node.params[1], slang)
        right = evaluate(node.params[2], slang)

        ops = {
            '大于': lambda a, b: a > b,
            '小于': lambda a, b: a < b,
            '等于': lambda a, b: a == b,
            '大于等于': lambda a, b: a >= b,
            '小于等于': lambda a, b: a <= b,
            '不等于': lambda a, b: a != b,
        }

        if op in ops and ops[op](left, right):
            return evaluate(node.params[3], slang)
        elif len(node.params) > 4:
            return evaluate(node.params[4], slang)
        return ''

    # ── 循环- ──
    if name == '循环-':
        if len(node.params) < 2:
            return ''
        ret = []
        while True:
            cond = evaluate(node.params[0], slang)
            if cond in ('True', 'true', '真', '1'):
                ret.append(evaluate(node.params[1], slang))
            else:
                break
        return ''.join(ret)

    return ''
