import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import re


def preprocess_expression(expr_str):
    print(f"Original expression: {expr_str}")

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

    print(f"Preprocessed expression: {expr_str}")
    return expr_str


def plot_sympy_expression(expr_str, xmin=-10, xmax=10, ymin=None, ymax=None):
    try:
        # Preprocess the expression
        expr_str = preprocess_expression(expr_str)

        # Create a SymPy symbol and parse the expression
        x = sp.Symbol('x', real=True)
        expr = sp.sympify(expr_str)

        # Create a lambda function for numerical evaluation
        f = sp.lambdify(x, expr, modules=['numpy',
                                          {'log': np.log, 'sqrt': np.sqrt, 'abs': np.abs,
                                           'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                                           'exp': np.exp}])

        # Create x values for plotting
        x_vals = np.linspace(xmin, xmax, 1000)

        # Evaluate y values, handling potential warnings
        with np.errstate(all='ignore'):
            y_vals = f(x_vals)

        # Remove any non-finite values
        mask = np.isfinite(y_vals)
        x_vals, y_vals = x_vals[mask], y_vals[mask]

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(x_vals, y_vals)

        # Set x-axis limits
        ax.set_xlim(xmin, xmax)

        # Set y-axis limits if provided, otherwise use data limits
        if ymin is not None and ymax is not None:
            ax.set_ylim(ymin, ymax)
        else:
            ymin, ymax = ax.get_ylim()
            ymin = min(ymin, 0)  # Ensure y-axis includes 0
            ax.set_ylim(ymin, ymax)

        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)

        # Add Cartesian coordinate system
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)

        # Add title with LaTeX rendering
        latex_expr = sp.latex(expr)
        ax.set_title(f"$f(x) = {latex_expr}$", fontsize=16)

        # Customize x and y labels
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('f(x)', fontsize=14)

        # Adjust layout to prevent clipping of labels
        plt.tight_layout()

        # Save the plot
        plt.savefig('sympy_plot.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Plot saved as 'sympy_plot.png'")

        # Calculate value at x = 2
        specific_x = 2
        y_at_2 = float(f(specific_x))
        print(f"Value at x = {specific_x}: {y_at_2}")

        return 'sympy_plot.png'

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return str(e)


# Example usage
expressions = [
    "x^2 + sin(x) + e^x",
    "2*x + 3(x+1)",
    "log(x) + ln(x) + π*x",
    "tan(x) + cos(2x)",
    "sqrt(x) + abs(x-3)",
    "x^2 - exp(x-3x^(-2x)-5)",
    "sin(x^3/10) * cos(exp(x/4)) + log(abs(x) + 1) / (1 + e^(-x^2)) - sqrt(abs(tan(x))) + (x^4 - 3x^2) / (x^6 + 1)"
]

for expression in expressions:
    print(f"\nProcessing: {expression}")
    # Adjust the plotting range for the complex function
    if "sin(x^3/10)" in expression:
        result = plot_sympy_expression(expression, xmin=-10, xmax=10, ymin=-5, ymax=5)
    else:
        result = plot_sympy_expression(expression, xmin=-5, xmax=5, ymin=-10, ymax=10)
    if result != 'sympy_plot.png':
        print(f"Failed to plot: {result}")