"""Example: verify shared scaling across multiple 3D items.

Expected result (visual check):
- A single 3D window titled "Multi-item scaling check" opens.
- The grid/ticks must cover BOTH the surface and the red points.
- The red points sit near the outer bounds of the grid (not clipped).
- The surface remains centered and properly scaled within the same grid.
- If scaling is incorrect, the grid will appear to fit the surface only,
  and the red points will appear outside the grid or compressed.
"""

import numpy as np
import mlpyqtgraph as mpg


@mpg.plotter
def main():
    extent = 5
    n = 40
    x = np.linspace(-extent, extent, n)
    y = np.linspace(-extent, extent, n)
    z = np.sin(np.hypot(*np.meshgrid(x, y, indexing='ij')))

    # Larger-range points to force global scaling across all items
    xp = np.array([-12, 0, 12])
    yp = np.array([-8, 0, 8])
    zp = np.array([-6, 0, 6])

    mpg.figure(title='Multi-item scaling check', layout_type='Qt')
    mpg.surf(x, y, z, colormap='CET-L10')
    mpg.points3(xp, yp, zp, color=(0.9, 0.1, 0.1, 1), size=6)
    ax = mpg.gca()
    ax.azimuth = 240


if __name__ == '__main__':
    main()
