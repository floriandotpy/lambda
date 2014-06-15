# -*- coding: utf-8 -*-

from .types import Environment, LispError, Closure
from .ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from .asserts import assert_exp_length, assert_valid_definition, assert_boolean
from .parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of the language.
"""


def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    """
        primitives
    """
    if is_boolean(ast):
        return ast
    elif is_integer(ast):
        return ast
    elif ast[0] == "quote":
        return ast[1]
    elif is_symbol(ast):
        return env.lookup(ast)

    if not is_list(ast):
        raise LispError("list expected")

    """
        unary functions
    """
    cmd = ast[0]
    if cmd == "atom":
        return is_atom(evaluate(ast[1], env))

    """
        binary functions
    """
    if cmd == "eq":
        return is_atom(evaluate(ast[1], env)) \
            and is_atom(evaluate(evaluate(ast[2], env), env)) \
            and evaluate(ast[1], env) == evaluate(ast[2], env)

    if cmd in ("+", "-", "/", "*", "mod", ">", "<"):
        v_1 = evaluate(ast[1], env)
        v_2 = evaluate(ast[2], env)
        if not (is_integer(v_1) and is_integer(v_2)):
            raise LispError("Arguments have to be integers.")
    if cmd == "+":
        return evaluate(ast[1], env) + evaluate(ast[2], env)
    if cmd == "-":
        return evaluate(ast[1], env) - evaluate(ast[2], env)
    if cmd == "/":
        return evaluate(ast[1], env) / evaluate(ast[2], env)
    if cmd == "*":
        return evaluate(ast[1], env) * evaluate(ast[2], env)
    if cmd == "mod":
        return evaluate(ast[1], env) % evaluate(ast[2], env)
    if cmd == ">":
        return evaluate(ast[1], env) > evaluate(ast[2], env)
    if cmd == "<":
        return evaluate(ast[1], env) < evaluate(ast[2], env)

    """
        ternary functions
    """
    if cmd == "if":
        if evaluate(ast[1], env) == True:
            return evaluate(ast[2], env)
        else:
            return evaluate(ast[3], env)

    """
        set and evaluate variables
    """
    # set variable
    if cmd == "define":
        # exactly 2 arguments
        if not len(ast) == 3:
            raise LispError("Wrong number of arguments")

        # first argument needs to be a symbol
        if not is_symbol(ast[1]):
            raise LispError("non-symbol")

        env.set(ast[1], evaluate(ast[2], env))

        # return anything
        return True


    """
        closures
    """

    # call closure
    if is_closure(ast[0]):
        if len(cmd.params) != len(ast)-1:
            raise LispError("wrong number of arguments, expected %d got %d" \
                % (len(cmd.params), len(ast)-1))

        # bound variables
        bound_vars = dict()
        for i, param in enumerate(cmd.params):
            value = evaluate(ast[1+i], env)
            bound_vars[param] = value

        # merge free and bound variables
        bound_env = cmd.env.extend(bound_vars)

        return evaluate(cmd.body, bound_env)

    # define closure
    if cmd == "lambda":
        # exactly 2 arguments
        if not len(ast) == 3:
            raise LispError("Wrong number of arguments")

        params = ast[1]
        body = ast[2]

        if not is_list(params):
            raise LispError("parameters of lambda need to be a list")

        return Closure(env, params, body)

    """
        lists
    """
    if cmd == "cons":
        return [ evaluate(ast[1], env) ] + evaluate(ast[2], env)
    if cmd == "head":
        if len(ast) >= 2:
            l = evaluate(ast[1], env)
            if l == []:
                raise LispError("empty list")
            return l[0]
        else:
            raise LispError("Cannot get element from empty list")
    if cmd == "tail":
        l = evaluate(ast[1], env)
        if l == []:
            raise LispError("empty list")
        return l[1:]
    if cmd == "empty":
        l = evaluate(ast[1], env)
        return l == []

    """
        everything that hasnt been evaluated yet: assume this is a function call
    """

    if is_symbol(ast[0]) or is_list(ast[0]):
        closure = evaluate(ast[0], env)
        return evaluate([closure] + ast[1:], env)

    raise LispError("not a function")