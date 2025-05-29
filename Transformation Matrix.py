import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

# Transformation functions

def rot_x(angle_deg):
    theta = np.radians(angle_deg)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta),  np.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rot_y(angle_deg):
    theta = np.radians(angle_deg)
    return np.array([
        [np.cos(theta), 0, np.sin(theta), 0],
        [0, 1, 0, 0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rot_z(angle_deg):
    theta = np.radians(angle_deg)
    return np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta),  np.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def translate(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

# 3D box points
box_points = np.array([
    [1, 1, 0, 1], [-1, 1, 0, 1], [-1, -1, 0, 1], [1, -1, 0, 1],
    [1, 1, 2, 1], [-1, 1, 2, 1], [-1, -1, 2, 1], [1, -1, 2, 1]
]).T

edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4),
         (0,4), (1,5), (2,6), (3,7)]

# Setup sliders
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.25, bottom=0.4)

# Initial transform values
init_rx, init_ry, init_rz = 30, 90, 30
init_tx, init_ty, init_tz = -1, -1, 3

# Create sliders
ax_rx = plt.axes([0.25, 0.30, 0.65, 0.03])
ax_ry = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_rz = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_tx = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_ty = plt.axes([0.25, 0.10, 0.65, 0.03])
ax_tz = plt.axes([0.25, 0.05, 0.65, 0.03])

s_rx = Slider(ax_rx, 'Rotate X°', 0, 360, valinit=init_rx)
s_ry = Slider(ax_ry, 'Rotate Y°', 0, 360, valinit=init_ry)
s_rz = Slider(ax_rz, 'Rotate Z°', 0, 360, valinit=init_rz)
s_tx = Slider(ax_tx, 'Translate X', -5, 5, valinit=init_tx)
s_ty = Slider(ax_ty, 'Translate Y', -5, 5, valinit=init_ty)
s_tz = Slider(ax_tz, 'Translate Z', -5, 5, valinit=init_tz)

#Draw box
def draw_box(rx, ry, rz, tx, ty, tz):
    ax.clear()

    # Compute centroid of the box
    centroid = np.mean(box_points[:3, :], axis=1).reshape(3, 1)

    # Translate box to origin for rotation
    centered = box_points.copy().astype(float)
    centered[:3, :] -= centroid

    # Apply rotation
    R = rot_z(rz) @ rot_y(ry) @ rot_x(rx)

    # Translate back, then apply user translation
    T = translate(tx, ty, tz)
    final_transform = T @ R

    transformed = final_transform @ np.vstack((centered[:3, :], np.ones((1, centered.shape[1]))))

    # Draw box edges
    for i, j in edges:
        ax.plot([transformed[0, i], transformed[0, j]],
                [transformed[1, i], transformed[1, j]],
                [transformed[2, i], transformed[2, j]], 'blue')

    ax.scatter(transformed[0], transformed[1], transformed[2], c='red')
    axis_length = 1.5
    x_axis = (T @ R @ np.array([axis_length, 0, 0, 1]))[:3]
    y_axis = (T @ R @ np.array([0, axis_length, 0, 1]))[:3]
    z_axis = (T @ R @ np.array([0, 0, axis_length, 1]))[:3]

    # Plot settings
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-6, 6)
    ax.set_box_aspect([1, 1, 1])
    ax.set_title("3D Box with Local Axes")
    fig.canvas.draw_idle()

# Initial draw
draw_box(init_rx, init_ry, init_rz, init_tx, init_ty, init_tz)

def update(val):
    draw_box(s_rx.val, s_ry.val, s_rz.val, s_tx.val, s_ty.val, s_tz.val)

s_rx.on_changed(update)
s_ry.on_changed(update)
s_rz.on_changed(update)
s_tx.on_changed(update)
s_ty.on_changed(update)
s_tz.on_changed(update)

plt.show()