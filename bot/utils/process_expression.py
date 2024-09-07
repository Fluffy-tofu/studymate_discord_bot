import re
import sympy as sp


class ProcessExpression:
    def __int__(self) -> None:
        super().__int__()

    def preprocess_expr(self, expr_str: str) -> str:
        # Replace '^' with '**' for exponentiation
        expr_str = re.sub(r'(\d+|x|\))\s*\^\s*(-?\d+|x|\()', r'\1**\2', expr_str)

        # Replace 'e^' or 'e**' with 'exp'
        expr_str = re.sub(r'e(\^|\*\*)', 'exp(', expr_str)

        # Ensure all 'exp' functions are properly closed
        open_count = 0
        new_expr = ""
        for char in expr_str:
            if char == '(':
                open_count += 1
            elif char == ')':
                open_count -= 1
            new_expr += char
            if open_count == 0 and new_expr.endswith('exp('):
                new_expr += ')'
        expr_str = new_expr

        # Replace 'ln' with 'log'
        expr_str = expr_str.replace('ln', 'log')

        # Replace standalone 'log' with 'log10'
        expr_str = re.sub(r'(?<!\w)log(?!\w|\()', 'log10', expr_str)

        # Add multiplication symbol '*' where implied
        expr_str = re.sub(r'(?<=\d)(?=[a-zA-Z(])', '*', expr_str)
        expr_str = re.sub(r'(?<=\))(?=\d|x)', '*', expr_str)

        # Replace π with pi
        expr_str = expr_str.replace('π', 'pi')

        # Ensure balanced parentheses
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

    def parse_expr(self, expr_str: str):
        expr_str= self.preprocess_expr(expr_str)
        expr = sp.sympify(expr_str)
        return expr
