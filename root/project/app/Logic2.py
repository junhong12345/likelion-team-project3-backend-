import os,re, sys,time,json 
from pathlib import Path 
import requests

class Logic2:
    def __init__(self):
        self.content = None
        self.result=  None

        #path 
        self.base_path = Path("/root/project")
        self.app_path = self.base_path / "app"
        self.report_path = self.base_path / "reports.json"
        self.upload_path = self.base_path / "uploads"
        self.result_path = self.base_path / "Logic2_result.json"
        
        self.department_name="관련부서"
    
    def delete_file(self):
        try:
            if os.path.isfile(self.result_path) and os.path.exists(self.result_path):
                os.remove(self.result_path)
                print(f"{self.result_path}파일 삭제 완료\n")
            else:
                print("Logic2 기존 결과 파일이 존재하지 않습니다.")
        except Exception as e:
            print(f'ERROR: {e}')
    def openfile(self):
        try:
            if os.path.isfile(self.report_path) and os.path.exists(self.report_path):
                print(f"{self.report_path} 파일이 존재합니다. ")
                with open(self.report_path, "r", encoding="utf-8") as f:
                    self.content = json.load(f)

            else:
                self.content = []       
        except Exception as e:
            print(f"ERROR: {e}")
            self.content = []

    def send_department(self):
        try:
            if len(self.content)==0:
                print("전달할 신고내역이 존재하지 않습니다.")
                self.result = {
                    "success" : False,
                    "message" : "전달할 신고 내역이 존재하지 않습니다."
                }
                return self.result
            
            latest_report = self.content[-1]
            print("===== 관련부서 전달 =====")

            print(f"부서 : {self.department_name}")

            print(f"신고번호 : {latest_report['reportId']}")

            print(f"제목 : {latest_report['title']}")

            print(f"내용 : {latest_report['content']}")

            print(f"주소 : {latest_report['address']}")

            print(f"이미지 : {latest_report['imageUrl']}")

            print("========================")
            self.result = {
                "success": True,
                "department": self.department_name,
                "reportId": latest_report.get("reportId"),
                "title": latest_report.get("title"),
                "category": latest_report.get("category"),
                "content": latest_report.get("content"),
                "address": latest_report.get("address"),
                "latitude": latest_report.get("latitude"),
                "longitude": latest_report.get("longitude"),
                "imageUrl": latest_report.get("imageUrl"),
                "status": "전달 완료"
            }
            with open(self.result_path, "w", encoding="utf-8") as f:
                json.dump(self.result, f,ensure_ascii=False,indent= 2)

            print(f"{self.result_path} 파일 저장 완료")

            return self.result


        except Exception as e:
            print(f"ERROR: {e}")
