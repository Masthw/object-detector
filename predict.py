import os
import cv2
import subprocess
import tempfile
from ultralytics import YOLO

# Caminhos
BASE_DIR = "."
MODEL_PATH = os.path.join('.', 'runs', 'detect', 'car_detector6', 'weights', 'best.pt')
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Solução alternativa: Converter o modelo para formato ONNX primeiro
def convert_to_onnx(pt_path, onnx_path):
    """Converte o modelo PyTorch para ONNX para evitar problemas de carregamento"""
    model = YOLO(pt_path)
    model.export(format="onnx")
    return onnx_path

# Tenta carregar o modelo diretamente, se falhar converte para ONNX
try:
    model = YOLO(MODEL_PATH)
    print("Modelo carregado diretamente com sucesso!")
except Exception as e:
    print(f"Erro ao carregar modelo: {e}")
    print("Convertendo para ONNX...")
    
    # Cria um arquivo temporário ONNX
    with tempfile.NamedTemporaryFile(suffix='.onnx', delete=False) as tmp:
        onnx_path = tmp.name
    
    # Converte o modelo
    convert_to_onnx(MODEL_PATH, onnx_path)
    
    # Carrega o modelo ONNX
    model = YOLO(onnx_path)
    print("Modelo carregado via ONNX com sucesso!")

# Limiar de confiança
THRESHOLD = 0.5

def process_image(image_path):
    img = cv2.imread(image_path)
    results = model(img)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > THRESHOLD:
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
            cv2.putText(img, results.names[int(class_id)].upper(),
                        (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

    out_path = image_path.replace(".jpg", "_out.jpg").replace(".png", "_out.png")
    cv2.imwrite(out_path, img)
    print(f"[OK] Imagem processada -> {out_path}")

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERRO] Não consegui abrir o vídeo {video_path}")
        return

    ret, frame = cap.read()
    if not ret:
        print(f"[ERRO] Não consegui ler frames do vídeo {video_path}")
        return

    H, W, _ = frame.shape

    out_path = video_path.replace(".mp4", "_out.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    frame_count = 0
    while ret:
        results = model(frame)[0]

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > THRESHOLD:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
                cv2.putText(frame, results.names[int(class_id)].upper(),
                            (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)

        out.write(frame)
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"[INFO] Processados {frame_count} frames...")

        ret, frame = cap.read()

    cap.release()
    out.release()
    print(f"[OK] Vídeo processado -> {out_path}")

if __name__ == "__main__":
    # Testa imagens
    if os.path.exists(IMAGES_DIR):
        for file in os.listdir(IMAGES_DIR):
            if file.endswith((".jpg", ".png")):
                process_image(os.path.join(IMAGES_DIR, file))

    # Testa vídeos
    if os.path.exists(VIDEOS_DIR):
        for file in os.listdir(VIDEOS_DIR):
            if file.endswith(".mp4"):
                process_video(os.path.join(VIDEOS_DIR, file))