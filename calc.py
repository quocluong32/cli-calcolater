
"""Simple interactive calculator.

Improvements:
- accepts words or symbols for operations
- accepts floats
- supports power (^ / pow / **), bitwise AND/OR/XOR (& | ^^), and sigma (summation)
- 'q' / 'quit' to exit
- input validation and division-by-zero handling
"""

def calculate(op, num1, num2):
    if op in ("add", "+"):
        return num1 + num2
    elif op in ("subtract", "-"):
        return num1 - num2
    elif op in ("multiply", "*"):
        return num1 * num2
    elif op in ("divide", "/"):
        return num1 / num2
    # power: '^' or 'pow' or '**'
    elif op in ("power", "pow", "^", "**"):
        return num1 ** num2
    # bitwise operations require integer inputs
    elif op in ("and", "&"):
        if int(num1) != num1 or int(num2) != num2:
            raise ValueError("Bitwise operations require integer values")
        return int(num1) & int(num2)
    elif op in ("or", "|"):
        if int(num1) != num1 or int(num2) != num2:
            raise ValueError("Bitwise operations require integer values")
        return int(num1) | int(num2)
    # use '^^' or 'xor' for bitwise xor to avoid ambiguity with power '^'
    elif op in ("xor", "^^"):
        if int(num1) != num1 or int(num2) != num2:
            raise ValueError("Bitwise operations require integer values")
        return int(num1) ^ int(num2)
    # sigma / summation: sum of integers from num1 to num2 (inclusive)
    elif op in ("sigma", "sum", "Σ"):
        if int(num1) != num1 or int(num2) != num2:
            raise ValueError("Sigma requires integer bounds")
        a = int(num1)
        b = int(num2)
        if a <= b:
            return sum(range(a, b + 1))
        else:
            return sum(range(b, a + 1))
    else:
        raise ValueError(f"Unknown operation: {op}")


def _parse_number(s):
    s = s.strip()
    if s.lower() in ("q", "quit", "exit"):
        raise KeyboardInterrupt
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Invalid number: {s!r}")


import ast


def _eval_node(node, env):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        raise NameError(f"name '{node.id}' is not defined")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, env)
        right = _eval_node(node.right, env)
        op = node.op
        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            return left / right
        if isinstance(op, ast.Pow):
            return left ** right
        if isinstance(op, ast.BitAnd):
            return int(left) & int(right)
        if isinstance(op, ast.BitOr):
            return int(left) | int(right)
        if isinstance(op, ast.BitXor):
            return int(left) ^ int(right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, env)
        if isinstance(node.op, ast.USub):
            return -operand
        if isinstance(node.op, ast.UAdd):
            return +operand
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def evaluate(src, env=None):
    if env is None:
        env = {}
    parsed = ast.parse(src, mode='exec')
    last = None
    for stmt in parsed.body:
        if isinstance(stmt, ast.Assign):
            if len(stmt.targets) != 1 or not isinstance(stmt.targets[0], ast.Name):
                raise ValueError("Invalid assignment")
            val = _eval_node(stmt.value, env)
            env[stmt.targets[0].id] = val
            last = val
        elif isinstance(stmt, ast.Expr):
            last = _eval_node(stmt.value, env)
        else:
            raise ValueError("Unsupported statement in evaluate()")
    return last, env


def main():
    print("Simple calculator. Type 'q' or 'quit' to exit.")
    env = {}
    while True:
        try:
            op = input("operation (add, subtract, multiply, divide, power(^), xor(^^), bitwise(&,|), sigma) or expression: ").strip()
            if op.lower() in ("q", "quit", "exit"):
                print("Bye.")
                break
            # If op matches known operations, use calculate flow
            known_ops = ("add", "+", "subtract", "-", "multiply", "*", "divide", "/", "power", "pow", "^", "**", "and", "&", "or", "|", "xor", "^^", "sigma", "sum", "Σ")
            if op.lower() in known_ops:
                a = input("first number: ").strip()
                if a.lower() in ("q", "quit", "exit"):
                    print("Bye.")
                    break
                b = input("second number: ").strip()
                if b.lower() in ("q", "quit", "exit"):
                    print("Bye.")
                    break
                try:
                    x = _parse_number(a)
                    y = _parse_number(b)
                except ValueError as e:
                    print(e)
                    continue
                try:
                    result = calculate(op, x, y)
                except ZeroDivisionError:
                    print("Error: division by zero")
                    continue
                except ValueError as e:
                    print(e)
                    continue
            else:
                try:
                    result, env = evaluate(op, env)
                except Exception as e:
                    print(e)
                    continue

            if result is None:
                print("OK")
            else:
                if isinstance(result, float) and result == int(result):
                    print(int(result))
                else:
                    print(result)

        except KeyboardInterrupt:
            print("\nInterrupted. Bye.")
            break


if __name__ == '__main__':
    main()
    

