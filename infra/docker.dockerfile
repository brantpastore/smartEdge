FROM python:3.12-slim

WORKDIR /app

# OpenCV + Qt runtime dependencies used by webcam and object detection flows.
RUN apt-get update && apt-get install -y --no-install-recommends \
	libgl1 \
	libglib2.0-0 \
	libx11-xcb1 \
	libxcb1 \
	libxcb-util1 \
	libxcb-image0 \
	libxcb-icccm4 \
	libxcb-keysyms1 \
	libxcb-randr0 \
	libxcb-render-util0 \
	libxcb-shape0 \
	libxcb-shm0 \
	libxcb-sync1 \
	libxcb-xfixes0 \
	libxcb-xinerama0 \
	libxcb-xkb1 \
	libxkbcommon0 \
	libxkbcommon-x11-0 \
	libice6 \
	libsm6 \
	libxext6 \
	libxrender1 \
	ffmpeg \
	fontconfig \
	fonts-dejavu-core \
	v4l-utils \
	&& rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV QT_QPA_FONTDIR=/usr/share/fonts/truetype/dejavu

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
RUN chmod +x /app/infra/start_services.sh

EXPOSE 8000

# Start FastAPI and object detection together.
CMD ["/app/infra/start_services.sh"]
