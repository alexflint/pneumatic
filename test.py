import sys
import inspect
import ast
import timeit

import long
import arithmetic
from arithmetic import *

print hello()

x1 = NumberExprAST(2.8)
x2 = NumberExprAST(100.)

x = BinaryExprAST('+', x1, x2)

y = NumberExprAST(50)

print evaluate_expression(x)
print execute(compile(x))


operation_map = {
    ast.Add: '+',
    ast.Sub: '-',
    ast.Mult: '*',
    ast.Div: '/'
};

refs = []
def ref(x):
    refs.append(x)
    return x

def from_ast(E):
    if isinstance(E, ast.BinOp):
        return BinaryExprAST(operation_map[type(E.op)],
                             ref(from_ast(E.left)),
                             ref(from_ast(E.right)))
    elif isinstance(E, ast.Num):
        return NumberExprAST(E.n)
    else:
        raise Exception('Invalid node: '+str(type(E)))

def from_func(f):
    lines, lineno = inspect.getsourcelines(f)
    T = ast.parse('\n'.join(lines))
    assert isinstance(T, ast.Module)
    assert len(T.body) == 1
    F = T.body[0]
    assert isinstance(F, ast.FunctionDef)
    assert len(F.body) == 1
    R = F.body[0]
    assert isinstance(R, ast.Return)
    return from_ast(R.value)

def llvm(f):
    expr = from_func(f)
    code = compile(expr)
    def impl():
        return execute(code)
    return impl


def foo():
    return 1+2+3

@llvm
def fast_foo():
    return 1+2+3

print foo()
print fast_foo()

sys.setrecursionlimit(100000)

fast_long = llvm(long.long)

def slow_long():
    return long.long()

print timeit.timeit('slow_long()', setup='from __main__ import slow_long')
print timeit.timeit('fast_long()', setup='from __main__ import fast_long')
