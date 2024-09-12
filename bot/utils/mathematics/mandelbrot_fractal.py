"""
NOT WRITTEN BY THE CREATOR OF THIS REPO!

Mandelbrot Set Visualization

This script generates and visualizes the Mandelbrot set, a famous example of a fractal in mathematics.

Mathematical Background:
------------------------
The Mandelbrot set is defined as the set of complex numbers c for which the function
f_c(z) = z^2 + c does not diverge when iterated from z = 0. In other words, a complex
number c is a member of the Mandelbrot set if, when starting with z_0 = 0 and applying
the iteration repeatedly:

z_(n+1) = z_n^2 + c

the absolute value of z_n remains bounded for all n > 0.

Key Properties:
1. If |z_n| > 2, the sequence will always diverge to infinity.
2. The Mandelbrot set is contained within the circle of radius 2 centered at the origin.
3. The set is connected, symmetric about the real axis, and has an infinitely complex boundary.

Implementation Details:
-----------------------
1. We use NumPy for efficient array operations, allowing vectorized computations.
2. The main algorithm iterates the function f_c(z) for each point in the complex plane.
3. We track the number of iterations before |z| > 2 (divergence) for each point.
4. The resulting array of iteration counts is used to color the visualization.
5. Matplotlib is used for plotting, including the LaTeX formula of the Mandelbrot function.

Usage:
------
Adjust the 'width', 'height', and 'max_iter' variables to change the resolution and detail level.
Different color maps can be explored by modifying the 'cmap' parameter in plt.imshow().

NOT WRITTEN BY THE CREATOR OF THIS REPO!
"""

import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO


class MandelBrotSetUtils:
    @staticmethod
    def mandelbrot(height, width, max_iter):
        """
        Generate the Mandelbrot set.

        Args:
        height, width (int): Dimensions of the output array.
        max_iter (int): Maximum number of iterations to determine if a point is in the set.

        Returns:
        numpy.ndarray: 2D array of iteration counts.
        """
        y, x = np.ogrid[-1.4:1.4:height * 1j, -2:0.8:width * 1j]
        c = x + y * 1j
        z = c
        divtime = max_iter + np.zeros(z.shape, dtype=int)

        for i in range(max_iter):
            z = z ** 2 + c
            diverge = z * np.conj(z) > 2 ** 2  # |z|^2 > 4
            div_now = diverge & (divtime == max_iter)
            divtime[div_now] = i
            z[diverge] = 2  # Avoid overflow

        return divtime

    @staticmethod
    def plot_mandelbrot(mandelbrot_set, cmap):
        """
        Plot the Mandelbrot set.

        Args:
        mandelbrot_set (numpy.ndarray): 2D array of iteration counts.
        """
        try:
            plt.figure(figsize=(12, 10))
            plt.imshow(mandelbrot_set, cmap=cmap, extent=[-2, 0.8, -1.4, 1.4])
            plt.title("Mandelbrot Set", fontsize=16)
            plt.xlabel("Re(c)", fontsize=12)
            plt.ylabel("Im(c)", fontsize=12)

            formula = r'$f_c(z) = z^2 + c,\quad z_0 = 0$'
            plt.text(0.5, -1.6, formula, fontsize=16, ha='center', va='center')

            plt.colorbar(label='Iteration count')
            plt.tight_layout()

            img_buffer: BytesIO = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()

            return {
                "img_buffer": img_buffer,
                "cmap": cmap
            }
        except Exception as e:
            print("An error occured while rendering the mandelbrot set!")
            return {
                "error": str(e)
            }
