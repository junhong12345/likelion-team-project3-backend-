# 🌿 무심천 Eco-Monitor Backend

> 시민이 무심천의 환경 문제를 신고하면, 신고 내용을 저장하고 담당 부서로 전달하는 백엔드 시스템입니다.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![REST API](https://img.shields.io/badge/REST-API-orange)
![Status](https://img.shields.io/badge/Status-Developing-success)

</p>

---

# 📌 Project Overview

무심천 Eco-Monitor는 시민이 무심천에서 발생하는 환경 문제를 신고하면,

백엔드에서 신고 데이터를 저장하고 담당 부서에 전달하는 시스템입니다.

현재 구현된 기능은 다음과 같습니다.

- ✅ 시민 신고 접수
- ✅ 담당 부서 전달

---

# 🏗️ System Architecture

```text
Client (React)

        │

        ▼

FastAPI REST API

        │

        ▼

reports.json 저장

        │

        ▼

Main Pipeline

        │

        ▼

Logic2

        │

        ▼

담당 부서 전달
```

---

# 🚀 Core Features

## 1️⃣ 시민 신고 (Citizen Report)

### 주요 기능

- 신고 접수 API 제공
- Base64 이미지 업로드
- 이미지 파일 저장
- 신고 번호 자동 생성
- 신고 데이터 저장

### 저장 데이터

```json
{
    "reportId": 1,
    "title": "불법 쓰레기 투기",
    "category": "환경",
    "content": "공원 입구에 쓰레기가 많이 쌓여 있습니다.",
    "address": "충청북도 청주시 상당구",
    "latitude": 36.63,
    "longitude": 127.49,
    "imageUrl": "/uploads/example.png"
}
```

---

## 2️⃣ 담당 부서 전달 (Department Notification)

신고가 접수되면 Main Pipeline이 실행되고 Logic2를 통해 담당 부서로 전달됩니다.

### 처리 과정

```text
Citizen Report

      │

      ▼

Save Report

      │

      ▼

Main Pipeline

      │

      ▼

Logic2

      │

      ▼

Department Notification
```

### 현재 구현 기능

- 최신 신고 조회
- 담당 부서 전달
- 전달 결과 저장
- 전달 로그 생성

---

# 📂 Project Structure

```text
project/

├── app/
│   └── main.py

├── main_pipeline.py

├── Logic2.py

├── reports.json

├── Logic2_result.json

└── uploads/
```

---

# ⚙️ Backend Workflow

```text
POST /api/reports

        │

        ▼

Image Upload

        │

        ▼

Save Report

        │

        ▼

Execute Main Pipeline

        │

        ▼

Logic2

        │

        ▼

Department Notification

        │

        ▼

Response
```

---

# 📡 REST API

## POST /api/reports

### Request

```json
{
    "title":"불법 쓰레기 투기",
    "category":"환경",
    "content":"공원 입구에 쓰레기가 많이 쌓여 있습니다.",
    "address":"충청북도 청주시 상당구",
    "latitude":36.63,
    "longitude":127.49,
    "imageUrl":"Base64 Image"
}
```

### Response

```json
{
    "success": true,
    "reportId": 1,
    "imageUrl": "/uploads/example.png",
    "pipeline": {
        "Logic2": {
            "success": true,
            "department": "관련부서",
            "status": "전달 완료"
        }
    },
    "message": "신고가 접수되었습니다."
}
```

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | FastAPI |
| API | REST API |
| Data Storage | JSON |
| Image Upload | Base64 |
| Server | Uvicorn |

---

# ▶️ Run

```bash
git clone https://github.com/your-github-id/musimcheon-eco-monitor-backend.git

cd musimcheon-eco-monitor-backend

pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000
```

---

# 📈 Development Status

| Feature | Status |
|----------|--------|
| 시민 신고 | ✅ Complete |
| 담당 부서 전달 | ✅ Complete |
| 신고 중복 탐지 | 🚧 In Progress |
| 이메일 알림 | 🚧 Planned |
| SMS 알림 | 🚧 Planned |
| Push 알림 | 🚧 Planned |

---

# 📌 Future Plans

- 신고 중복 탐지 기능
- 이메일 알림
- SMS 알림
- Push 알림
- 관리자 페이지
- DB 연동 (MySQL)

---

# 👨‍💻 Team

**멋쟁이사자처럼 Team Project 2**

**Project : 무심천 Eco-Monitor**
