import os,re, sys,time,json
from pathlib import Path 

from Logic2 import Logic2

class main_pipeline:
    def __init__(self):
        self.content = None
        self.result = None

    def run(self):
        try:
            logic2 = Logic2()
            logic2.delete_file()
            logic2.openfile()
            logic2_result = logic2.send_department()
            
            return {
                "Logic2": logic2_result
            }
        except Exception as e:
            print(f"ERROR : {e}")

    
