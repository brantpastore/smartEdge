import cv2, time, logging
from smart_edge.core.logging import logger

class Webcam:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.flip_enabled = False
        self.blur_enabled = False
        self.capture_requested = False

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Failed to read frame from webcam")

        key = cv2.waitKey(1) & 0xFF
        if key == ord('f'):
            self.flip_enabled = not self.flip_enabled

        if key == ord('b'):
            self.blur_enabled = not self.blur_enabled

        if key == ord('c'):
            self.capture_requested = True

        if key == ord('q'):
            self.release()

        if self.capture_requested:
            self.capture_frame()

        if self.blur_enabled:
            frame = self.blur_frame(frame)

        if self.flip_enabled:
            frame = self.flip_frame(frame)

        return frame, False
    
    def capture_frame(self):
        capture_filename = f'screen_captures/{int(time.time())}_captured_frame.jpg'
        self.save_frame(capture_filename)
        self.capture_requested = False
    
    def save_frame(self, filename):
        ret, frame = self.cap.read() # Simplified for direct capture
        if not ret:
            logger.error("Failed to capture frame from webcam")
            raise Exception("Failed to capture frame from webcam")
        
        cv2.imwrite(filename, frame)
        print(f"Frame captured and saved as '{filename}'")
        logger.info(f"Captured frame saved as '{filename}'")
        logger.debug(f"Captured frame saved as '{filename}'")
        
    def show_frame(self, frame):
        cv2.imshow('Webcam', frame)
        # If the user clicks X on the OpenCV window, window visibility becomes < 1.
        is_visible = cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE)
        if is_visible < 1:
            self.release()

    def blur_frame(self, frame):
        return cv2.blur(frame, (15, 15), 0)
        logger.debug("Applied blur to the frame")
    
    def flip_frame(self, frame):
        return cv2.flip(frame, 1)  # Flip the frame horizontally

    def draw_detections(self, frame, results):
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            class_id = int(box.cls[0])
            label = f"{class_id}: {confidence:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            logger.debug(f"Detection: {label} at [{x1}, {y1}, {x2}, {y2}]")
    

    def release(self):
        logger.info("Releasing webcam resources...")
        self.cap.release()
        logger.info("Closing webcam window...")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    webcam = Webcam()
    try:
        while True:
            frame, _ = webcam.read_frame()
            webcam.show_frame(frame)
    except Exception as e:
            print("Failed to read frame from webcam: ", e)