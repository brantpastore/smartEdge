Focus: Computer Vision (OpenCV), FastAPI, Docker, IoT Edge Devices, Redis.

Build a containerized Python application that simulates running on an IoT Edge device (like a Raspberry Pi or Jetson Nano) to analyze a video stream, detect objects or faces, and stream the metadata to a central server.

        A Python script using OpenCV to process a video feed (or webcam) and run a lightweight pre-trained object detection model (like YOLOv8 or an OpenCV Haar Cascade).

        Wrap this edge logic inside a Docker container, simulating an IoT Edge deployment.

        Use FastAPI on the edge to expose a control API (e.g., to adjust detection sensitivity or toggle the feed).

        Use Redis as a local message broker/cache to handle rapid, real-time alert events on the edge before syncing them to a cloud database.

## Quick Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python Webcam/webcam.py
```

## Controls

- `f`: Toggle horizontal flip on/off.
- `b`: Toggle blur on/off.
- `c`: Capture and save one frame as `<unix_timestamp>_captured_frame.jpg`.
- `q`: Quit and release webcam resources.
- Window `X`: Close window and quit.

If OpenCV/Qt fails to start (`xcb` plugin error), install runtime GUI libs:

```bash
sudo apt update
sudo apt install -y libsm6 libice6 libxrender1 libxext6
ldd .venv/lib/python3.12/site-packages/cv2/qt/plugins/platforms/libqxcb.so | grep "not found" || true
```

## WSL Notes (USB + Permissions)

If using WSL, pass the webcam from Windows first (PowerShell as Administrator):

```powershell
usbipd list
usbipd bind --busid <BUSID>
usbipd attach --wsl --busid <BUSID>
```

In WSL, verify devices and video permissions:

```bash
ls /dev/video*
v4l2-ctl --list-devices
id
```

If needed, install tools and add your user to the video group:

```bash
sudo apt update && sudo apt install -y v4l-utils
sudo usermod -aG video $USER
```

After group changes, restart WSL and re-check `id`.

Use the virtual environment Python, not `/usr/bin/python3`, when running this project.