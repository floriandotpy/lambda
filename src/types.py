# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The LispError class you can have for free :)
"""


class LispError(Exception):
    """General lisp error class."""
    pass


class Closure:
    def __init__(self, env, params, body):
        self.env = env
        self.params = params
        self.body = body

    def __str__(self):
        return "<closure/%d>" % len(self.params)


class Environment:
    def __init__(self, variables=None):
        self.variables = variables if variables else {}

    def lookup(self, symbol):
        if symbol in self.variables:
            return self.variables[symbol]
        else:
            raise LispError(symbol)

    def extend(self, variables):
        # add variables, existing values of the same symbol will be overwritten
        new_variables = dict(self.variables.items() + variables.items())
        return Environment(new_variables)

    def set(self, symbol, value):
        if symbol in self.variables:
            raise LispError("already defined")
        else:
            self.variables[symbol] = value

    def __str__(self):
        return "<environment> %s" % self.variables

