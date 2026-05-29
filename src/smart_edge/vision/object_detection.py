from ultralytics import YOLO
from src.smart_edge.core.logging import setup_logging
from src.smart_edge.vision.webcam import Webcam
from datetime import datetime
import os
import argparse

# https://docs.ultralytics.com/guides/yolo26-training-recipe
# YOLO26m	Higher accuracy with moderate compute	Smaller batches (16-32)
# were going to use Ultralytics YOLO26m (very strong accuracy/speed balance)
class ObjectDetection:
    def __init__(self, model_path='yolo26m.pt'):
        self.model = YOLO(model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SmartEdge Object Detection")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--model", type=str, default="yolo26m.pt", help="Path to YOLO model")
    args = parser.parse_args()

    log_level = "DEBUG" if args.debug else "INFO"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/object_detection_{timestamp}.log"
    logger = setup_logging('src/smart_edge/core/config.json', log_filename, level=log_level)
    
    logger.info(f"Starting object detection with level: {log_level}")
    logger.debug("Debug logging is enabled")
    
    webcam = Webcam()
    detector = ObjectDetection(model_path=args.model)
    try:
        while True:
            frame, _ = webcam.read_frame()
            # Filter detections to class dog (COCO dog class is id 16)
            # COCO dog class id is 16.
            # We set imgsz to 416 for faster inference
            results = detector.model.predict(source=frame, classes=[16], imgsz=416, verbose=False)
            dog_count = len(results[0].boxes) if results else 0
            if dog_count > 0:
                print(f"Detected {dog_count} dog(s) in the frame.")
                webcam.draw_detections(frame, results[0])
            
            webcam.show_frame(frame)


    except KeyboardInterrupt:
        pass
    finally:
        webcam.release()