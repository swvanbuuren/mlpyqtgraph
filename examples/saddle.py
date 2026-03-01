"""
Basic example that shows a saddle surface plot and the corresponding points.
"""

import numpy as np
import mlpyqtgraph as mpg
from PIL import Image
import os


@mpg.plotter(projection='orthographic')
def main():
    """ Examples with surface plots """
    nx, ny = 20, 20
    x = np.linspace(-8, 8, nx)
    y = np.linspace(-8, 8, ny)
    z = 0.1 * ((x.reshape(ny,1) ** 2) - (y.reshape(1,nx) ** 2))

    xp = np.repeat(x, y.size)
    yp = np.tile(y, x.size)
    zp = z.flatten()

    mpg.figure(title='Saddle example')
    mpg.surf(x, y, z)
    mpg.points3(xp, yp, zp, color=(0.8, 0.1, 0.1, 1), size=4)
    ax = mpg.gca()
    ax.azimuth = 240
    ax.export('saddle_still.png')

    # create an animated PNG (APNG) with optimized settings
    # Use 3-degree steps (120 frames instead of 360) for smoother playback
    frames = []
    frame_paths = []
    
    for az in range(0, 360, 2):
        ax.azimuth = az
        frame_path = f'saddle_{az:03d}.png'
        ax.export(frame_path)
        frame_paths.append(frame_path)
    
    # Load all frames and normalize DPI to prevent Firefox resampling
    # Firefox scales images based on DPI metadata - we set it to 96 DPI (standard web DPI)
    for frame_path in frame_paths:
        img = Image.open(frame_path)
        frames.append(img)
        os.remove(frame_path)
    
    # Save as animated PNG with 50ms per frame (20 fps) and infinite loop
    # 50ms duration is more compatible with Firefox and provides smooth playback
    # Explicitly set DPI in the output file to ensure consistent display
    img_fmt = 'gif'
    frames[0].save(
        f'saddle_animated.{img_fmt}',
        save_all=True,
        append_images=frames[1:],
        duration=40,
        loop=0,
        optimize=True,
        format=img_fmt
    )
    
    print("Done")


if __name__ == '__main__':
    main()
