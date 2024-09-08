from typing import Dict, Union, Optional
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

from bot.utils.process_expression import ProcessExpression


def plot_sympy_expression(
    expr_str: str,
    xmin: int = -10,
    xmax: int = 10,
    ymin: Optional[int] = None,
    ymax: Optional[int] = None
) -> Dict[str, Union[BytesIO, int, float, str]]:
    """
    Plot a sympy expression and return the plot as a BytesIO object.

    This function takes a mathematical expression as a string, parses it,
    creates a plot of the function, and returns the plot as an image buffer
    along with the plot's x and y limits.

    Args:
        expr_str (str): The mathematical expression to plot.
        xmin (int, optional): The minimum x-value for the plot. Defaults to -10.
        xmax (int, optional): The maximum x-value for the plot. Defaults to 10.
        ymin (Optional[int], optional): The minimum y-value for the plot. Defaults to None.
        ymax (Optional[int], optional): The maximum y-value for the plot. Defaults to None.

    Returns:
        Dict[str, Union[BytesIO, int, float, str]]: A dictionary containing:
            - 'image': BytesIO object containing the plot image
            - 'xmin': The minimum x-value of the plot
            - 'xmax': The maximum x-value of the plot
            - 'ymin': The minimum y-value of the plot
            - 'ymax': The maximum y-value of the plot
            - 'error': An error message string if an error occurred (None otherwise)
    """
    try:
        expr: sp.Expr = ProcessExpression.parse_expr(expr_str)
        print(expr)
        x: sp.Symbol = sp.Symbol('x', real=True)

        f: callable = sp.lambdify(x, expr, modules=['numpy',
                                          {'log': np.log, 'sqrt': np.sqrt, 'abs': np.abs,
                                           'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                                           'exp': np.exp}])

        x_vals: np.ndarray = np.linspace(xmin, xmax, 1000)

        with np.errstate(all='ignore'):
            y_vals: np.ndarray = f(x_vals)

        mask: np.ndarray = np.isfinite(y_vals)
        x_vals, y_vals = x_vals[mask], y_vals[mask]

        if len(x_vals) == 0:
            raise ValueError("No valid data points to plot. The function might not be defined in the given range.")

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(x_vals, y_vals)

        ax.set_xlim(xmin, xmax)

        if ymin is not None and ymax is not None:
            ax.set_ylim(ymin, ymax)
        else:
            ymin, ymax = ax.get_ylim()
            ymin = min(ymin, 0)
            ax.set_ylim(ymin, ymax)

        ax.grid(True, linestyle='--', alpha=0.7)

        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)

        latex_expr: str = sp.latex(expr)
        ax.set_title(f"$f(x) = {latex_expr}$", fontsize=16)

        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('f(x)', fontsize=14)

        plt.tight_layout()

        img_buffer: BytesIO = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()

        return {
            'image': img_buffer,
            'xmin': xmin,
            'xmax': xmax,
            'ymin': ymin,
            'ymax': ymax
        }

    except Exception as e:
        print(f"An error occurred while plotting: {str(e)}")
        return {
            'error': str(e)
        }
