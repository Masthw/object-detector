from ultralytics import YOLO


model = YOLO('yolov8n.yaml')

results = model.train(
    data="dataset.yaml",
    epochs=20,
    name="car_detector",
    device="cpu",      
    batch=4,                  
    imgsz=640,
    save=True,
    save_period=5,
    amp=True,
    )

model.export(format="onnx")