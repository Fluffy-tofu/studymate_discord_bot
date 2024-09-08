import re
from typing import Union
import sympy as sp


class ProcessExpression:
    """
    A utility class for processing and parsing mathematical expressions.

    This class provides static methods to preprocess and parse mathematical
    expressions, preparing them for use with sympy and other mathematical operations.
    """

    @staticmethod
    def preprocess_expr(expr_str: str) -> str:
        """
        Preprocess a mathematical expression string to prepare it for parsing.

        This method performs several transformations on the input string:
        - Replaces '^' with '**' for exponentiation
        - Converts 'e^' or 'e**' to 'exp('
        - Replaces 'ln' with 'log' and standalone 'log' with 'log10'
        - Adds implicit multiplication symbols
        - Replaces 'π' with 'pi'
        - Ensures balanced parentheses

        Args:
            expr_str (str): The input mathematical expression string.

        Returns:
            str: The preprocessed expression string.
        """
        expr_str = re.sub(r'(\d+|x|\))\s*\^\s*(-?\d+|x|\()', r'\1**\2', expr_str)
        expr_str = re.sub(r'e(\^|\*\*)', 'exp(', expr_str)

        open_count: int = 0
        new_expr: str = ""
        for char in expr_str:
            if char == '(':
                open_count += 1
            elif char == ')':
                open_count -= 1
            new_expr += char
            if open_count == 0 and new_expr.endswith('exp('):
                new_expr += ')'
        expr_str = new_expr

        expr_str = expr_str.replace('ln', 'log')
        expr_str = re.sub(r'(?<!\w)log(?!\w|\()', 'log10', expr_str)
        expr_str = re.sub(r'(?<=\d)(?=[a-zA-Z(])', '*', expr_str)
        expr_str = re.sub(r'(?<=\))(?=\d|x)', '*', expr_str)
        expr_str = expr_str.replace('π', 'pi')

        open_count = 0
        for char in expr_str:
            if char == '(':
                open_count += 1
            elif char == ')':
                open_count -= 1
            if open_count < 0:
                expr_str = '(' + expr_str
                open_count = 0
        expr_str += ')' * open_count

        return expr_str

    @staticmethod
    def parse_expr(expr_str: str) -> sp.Expr:
        """
        Parse a preprocessed mathematical expression string into a sympy expression.

        This method first preprocesses the input string using the preprocess_expr method,
        then converts it into a sympy expression using sympy.sympify.

        Args:
            expr_str (str): The input mathematical expression string.

        Returns:
            sympy.Expr: The parsed sympy expression.
        """
        expr_str = ProcessExpression.preprocess_expr(expr_str)
        expr = sp.sympify(expr_str)
        return expr
