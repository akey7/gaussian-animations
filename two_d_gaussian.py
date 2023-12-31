import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import cm
from math import exp


def two_d_gaussian(points = 100,
                   a = 1.,
                   min_x = -4.,
                   min_y = -4.,
                   max_x = 4.,
                   max_y = 4.,
                   x0 = 0.,
                   y0 = 0.,
                   var_x = 1.,
                   var_y = 1.
):
    xs = np.linspace(min_x, max_x, points)
    ys = np.linspace(min_y, max_y, points)
    zs = np.zeros((points, points), np.float64)

    for ix, x in enumerate(xs):
        for iy, y in enumerate(ys):
            zs[ix, iy] = a * exp(-((x-x0)**2/2/var_x + (y-y0)**2/2/var_y))

    return xs, ys, zs


def main():
    dpi = 100
    width = 1080 / dpi
    height = 1920 / 2 / dpi
    seconds = 10
    frame_rate_ms = 33
    bgcolor = "#1E1E1E"
    line_color = "#73FBD3"
    axis_color = "#01BAEF"
    annotation_color = "#FFFFFF"
    # heading_text_color = "#FC7753"

    ms_per_frame = 33
    frames = 300
    x0_steps = np.concatenate([np.linspace(-4., 0., frames // 3), np.zeros(frames // 3), np.linspace(0., 4., frames // 3)])
    y0_steps = np.concatenate([np.linspace(-4., 0., frames // 3), np.zeros(frames // 3), np.linspace(0., 4., frames // 3)])
    var_x_steps = np.concatenate([np.ones(frames // 3), np.linspace(1., 7., frames // 6), np.linspace(7., 1., frames // 6), np.ones(frames // 3)])
    var_y_steps = np.concatenate([np.ones(frames // 3), np.linspace(1., 7., frames // 6), np.linspace(7., 1., frames // 6), np.ones(frames // 3)])
    a_steps = np.concatenate([np.linspace(0., 1., frames // 3), np.ones(frames // 3), np.linspace(1., 0., frames // 3)])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(bgcolor)
    fig.set_facecolor(bgcolor)
    ax.tick_params(axis="x", colors=axis_color)
    ax.tick_params(axis="y", colors=axis_color)
    ax.tick_params(axis="z", colors=axis_color)

    def init_func():
        xs, ys, zs = two_d_gaussian(x0=x0_steps[0], y0=y0_steps[0], var_x=var_x_steps[0], var_y=var_y_steps[0], a=a_steps[0])
        xs, ys = np.meshgrid(xs, ys)
        ax.set_xlabel("x", size=15, color=axis_color)
        ax.set_ylabel("y", size=15, color=axis_color)
        ax.set_zlabel("z", size=15, color=axis_color)
        ax.set_xlim(-4., 4.)
        ax.set_ylim(-4., 4.)
        ax.set_zlim(0., 1.)
        sfc = ax.plot_surface(xs, ys, zs, cmap=cm.plasma, linewidth=0, antialiased=True)
        return sfc,

    def update(frame):
        for coll in ax.collections:
            coll.remove()
        xs, ys, zs = two_d_gaussian(x0=x0_steps[frame], y0=y0_steps[frame], var_x=var_x_steps[frame], var_y=var_y_steps[frame], a=a_steps[frame])
        xs, ys = np.meshgrid(xs, ys)
        sfc = ax.plot_surface(xs, ys, zs, cmap=cm.plasma, linewidth=0, antialiased=True)
        print(f"Rendered frame {frame}")
        return sfc,

    ani = animation.FuncAnimation(fig=fig, func=update, init_func=init_func, frames=300, interval=ms_per_frame)
    ani.save(filename=os.path.join("output", "single_2d_gaussian.mp4"), writer="ffmpeg")


if __name__ == "__main__":
    main()
