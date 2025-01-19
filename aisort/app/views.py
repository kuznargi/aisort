import cv2
from ultralytics import YOLO
from django.http import StreamingHttpResponse


def gen_frames_yolo():
    cap = cv2.VideoCapture(0)
    
    # Шаг 2: Загружаем модель (не .txt, а .pt!)
    model = YOLO('best.pt')  # например, best.pt
    model_names = list(model.names.values())

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        results = model.predict(frame, conf=0.25)  
        
        # Берём список детекций (bounding boxes)
        boxes = results[0].boxes if len(results) > 0 else []

        # Рисуем bounding-box для каждого обнаруженного объекта
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls_id = int(box.cls[0])       # индекс класса
            conf = float(box.conf[0])      # уверенность

            # Шаг 3: Вместо model.names[cls_id], берём название из custom_classes
            cls_id = int(box.cls[0])
            if 0 <= cls_id < len(model_names):
                # Например, склеим названия через "/"
                class_name = f"{model_names[cls_id]}"
            else:
                # fallback
                class_name = model_names[cls_id]  # или "Unknown"

            # Рисуем прямоугольник и текст
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
            cv2.putText(
                frame,
                f"{class_name} {conf:.2f}",
                (int(x1), int(y1)-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                1
            )
        
        # Кодируем кадр в JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()

def video_feed_yolo(request):
    return StreamingHttpResponse(
        gen_frames_yolo(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
