from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import json
import base64
import uuid

from main_pipeline import main_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]

)

BASE_PATH = Path("/root/project")
REPORTS_PATH = BASE_PATH / "reports.json"
UPLOAD_DIR = BASE_PATH / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads"
)

class API_Model(BaseModel):
    title: str
    category: str
    content: str
    address: str
    latitude: float
    longitude: float
    imageUrl: str

@app.get("/")
def root():
    return "OK"

@app.get("/health_check")
def health_check():
    return "FastAPI_Server_is_OK"

def save_base64_image(image_data: str) -> str:
    try:
        header, encoded = image_data.split(",", 1)

        if "image/png" in header:
            extension = "png"
        elif "image/jpeg" in header:
            extension = "jpg"
        elif "image/webp" in header:
            extension = "webp"
        else:
            raise ValueError("지원하지 않는 이미지 형식입니다.")

        filename = f"{uuid.uuid4()}.{extension}"
        file_path = UPLOAD_DIR / filename

        image_bytes = base64.b64decode(encoded)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        return f"/uploads/{filename}"

    except Exception as e:
        raise ValueError(f"이미지 저장 실패: {e}")


@app.post("/api/reports")
def create_report(request: API_Model):
    data = request.model_dump()

    # Base64 이미지이면 실제 파일로 저장
    if data["imageUrl"].startswith("data:image"):
        saved_image_url = save_base64_image(data["imageUrl"])
        data["imageUrl"] = saved_image_url

    if REPORTS_PATH.exists():
        with open(REPORTS_PATH, "r", encoding="utf-8") as f:
            reports = json.load(f)

    else:
        reports = []

    report_id = len(reports) + 1
    data["reportId"] = report_id
    reports.append(data)

    with open(REPORTS_PATH, "w", encoding="utf-8") as f:
        json.dump(
            reports,
            f,
            ensure_ascii=False,
            indent=4
        )
    pipeline = main_pipeline()
    pipeline_result = pipeline.run()

    return {
        "success": True,
        "reportId": report_id,
        "imageUrl": data["imageUrl"],
        "pipeline": pipeline_result,
        "message": "신고가 접수되었습니다."
    }

