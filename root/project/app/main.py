from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import json
import base64
import uuid

from main_pipeline import main_pipeline
from fastapi import FastAPI, HTTPException

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
LOGIC2_RESULT_PATH = BASE_PATH / "Logic2_result.json"
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

class StatusUpdate(BaseModel):
    status: str

    
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

@app.get("/api/logic2")
def get_logic2_result():
    if not LOGIC2_RESULT_PATH.exists():
        return {
            "success": True,
            "message" : "데이터 가져오기 실패"
        }

    try:
        with open(LOGIC2_RESULT_PATH, "r", encoding= "utf-8") as f:
            logic2_result=  json.load(f)    #LOGIC2_RESULT_PATH 경로 파일 가져오기 json 형식으로

            return {
                "success": True,
                "data": logic2_result,
                "message" : "데이터 가져오기 성공"
            } 
    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "Logic2_result.json 파일 형식이 올바르지 않습니다."
        }
    
    except Exception as e:
        print(f"ERROR: {e}")
        return {
            "success": False,
            "message": str(e)
        }

@app.patch("/api/reports/{report_id}/status")
def update_report_status(
    report_id: int,
    status_data: StatusUpdate
):

    try:
        if not REPORTS_PATH.exists():
            raise HTTPException(
                status_code=404,
                detail="reports.json 파일이 존재하지 않습니다."
            )

        with open(REPORTS_PATH, "r", encoding="utf-8") as f:
            reports = json.load(f)

        target_report = None

        for report in reports:
            if report.get("reportId") == report_id:
                report["status"] = status_data.status
                target_report = report
                break

        if target_report is None:
            raise HTTPException(
                status_code=404,
                detail=f"reportId {report_id} 신고를 찾을 수 없습니다."
            )

        with open(REPORTS_PATH, "w", encoding="utf-8") as f:
            json.dump(
                reports,
                f,
                ensure_ascii=False,
                indent=4
            )

        return {
            "success": True,
            "message": "신고 상태가 변경되었습니다.",
            "data": target_report
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
