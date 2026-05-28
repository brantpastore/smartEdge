from ultralytics import YOLO
from src.smart_edge.vision.webcam import Webcam

# https://docs.ultralytics.com/guides/yolo26-training-recipe
# YOLO26m	Higher accuracy with moderate compute	Smaller batches (16-32)
# were going to use Ultralytics YOLO26m (very strong accuracy/speed balance)
class ObjectDetection:
    def __init__(self, model_path='yolo26m.pt'):
        self.model = YOLO(model_path)

if __name__ == "__main__":
    webcam = Webcam()
    detector = ObjectDetection()
    try:
        while True:
            frame, _ = webcam.read_frame()
            # Filter detections to class dog (COCO dog class is id 16)
            # COCO dog class id is 16.
            # We set imgsz to 416 for faster inference
            results = detector.model.predict(source=frame, classes=[16], imgsz=416, verbose=False)
            dog_count = len(results[0].boxes) if results else 0
            if dog_count > 0:
                webcam.draw_detections(results[0])
                print(f"Detected dogs: {dog_count}")


    except KeyboardInterrupt:
        pass
    finally:
        webcam.release()