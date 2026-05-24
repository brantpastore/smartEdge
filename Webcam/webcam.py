import cv2, time

class Webcam:
    flip_enabled = False
    blur_enabled = False
    capture_frame = False

    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Failed to read frame from webcam")

        key = cv2.waitKey(1) & 0xFF
        if key == ord('f'):
            if self.flip_enabled:
                self.flip_enabled = False
            else:
                self.flip_enabled = True

        if key == ord('b'):
            if self.blur_enabled:
                self.blur_enabled = False
            else:
                self.blur_enabled = True

        if key == ord('c'):
            if self.capture_frame:
                self.capture_frame = False
            else:
                self.capture_frame = True

        if key == ord('q'):
            self.release()

        if self.capture_frame:
            self.capture_frame = False
            cv2.imwrite(f'{int(time.time())}_captured_frame.jpg', frame)
            print("Frame captured and saved as 'captured_frame.jpg'")

        if self.blur_enabled:
            frame = cv2.blur(frame, (15, 15), 0)

        if self.flip_enabled:
            frame = cv2.flip(frame, 1)  # Flip the frame horizontally

        cv2.imshow('Webcam', frame)  # Update the displayed frame

        # If the user clicks X on the OpenCV window, window visibility becomes < 1.
        is_visible = cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE)
        if is_visible < 1:
            self.release()

        return frame, False
    
    def capture_frame(self, filename):
        ret, frame = self.capture_frame()
        if not ret:
            raise Exception("Failed to capture frame from webcam")
        
        cv2.imwrite(filename, frame)
    

    def release(self):
        print("Releasing webcam resources...")
        self.cap.release()
        print("Closing webcam window...")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    webcam = Webcam()
    try:
        while True:
            frame = webcam.read_frame()
    except Exception as e:
            print("Failed to read frame from webcam: ", e)