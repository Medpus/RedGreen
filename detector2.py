import sys
import time
import openvr
import tkinter as tk
import threading

# Initialize OpenVR
openvr.init(openvr.VRApplication_Scene)

# Create a Tkinter window
root = tk.Tk()
root.attributes('-fullscreen', True)  # Launch in fullscreen

# Create a canvas to change its color
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

def get_vr_poses():
    poses = []  # will be populated with proper type after first call
    prev_pose = [None, None, None]
    threshold = 0.0001  # Define your threshold here

    while True:
        poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
        hmd_pose = poses[1] # 1 for controller, 0 for HMD
        current_pose = [hmd_pose.mDeviceToAbsoluteTracking[i][3] for i in range(3)]

        if all(prev_pose):
            changes = [abs(current - prev) for current, prev in zip(current_pose, prev_pose)]
            if any(change > threshold for change in changes):
                # If the current color is red, change it to green, and vice versa
                current_color = canvas.cget("bg")
                new_color = "green" if current_color == "red" else "red"
                canvas.config(bg=new_color)
                root.update()

        prev_pose = current_pose
        print(*current_pose)
        sys.stdout.flush()

# Start the VR pose getting in a separate thread
threading.Thread(target=get_vr_poses, daemon=True).start()

# Start the Tkinter event loop
root.mainloop()

# Shut down OpenVR
openvr.shutdown()