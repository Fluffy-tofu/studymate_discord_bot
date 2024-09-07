import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

from bot.utils.process_expression import ProcessExpression


def plot_sympy_expression(expr_str, xmin=-10, xmax=10, ymin=None, ymax=None):
    try:
        # Parse the expression
        expr = ProcessExpression.parse_expr(expr_str)
        x = sp.Symbol('x', real=True)

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

        # Check if we have valid data to plot
        if len(x_vals) == 0:
            raise ValueError("No valid data points to plot. The function might not be defined in the given range.")

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

        # Save the plot to a BytesIO object
        img_buffer = BytesIO()
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
        # Log the error (you might want to use a proper logging system)
        print(f"An error occurred while plotting: {str(e)}")
        return {
            'error': str(e)
        }
