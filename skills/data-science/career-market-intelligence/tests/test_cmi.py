import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/"scripts"/"cmi.py"

class CMITest(unittest.TestCase):
    def run_cli(self,*args,check=True):
        return subprocess.run([sys.executable,str(CLI),*map(str,args)],capture_output=True,text=True,check=check)

    def make_postings(self,path):
        rows=[]
        for i in range(60):
            desc="SQL Python Excel data visualization. Minimum 3 years of experience. Bachelor's degree."
            if i<42: desc += " Power BI."
            if i<18: desc += " Snowflake."
            rows.append({"id":f"d{i}","title":"Senior Data Analyst","location":"Denver, CO","posted_date":f"2026-{1+(i%6):02d}-{1+(i%20):02d}","description":desc})
        for i in range(40):
            desc="Excel project management stakeholder management. Minimum 2 years of experience."
            if i<4: desc += " SQL."
            rows.append({"id":f"p{i}","title":"Project Coordinator","location":"Denver, CO","posted_date":"2026-05-01","description":desc})
        with path.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

    def make_outcomes(self,path):
        rows=[]
        # 80 records: SQL group 40 with 24 hires, no-SQL group 40 with 8 hires.
        for i in range(80):
            has=i<40; hired=(i<24 if has else i<48)
            rows.append({"candidate_id":i,"target_title":"Senior Data Analyst","location":"Denver","status":"hired" if hired else "rejected","skills":"SQL;Python" if has else "Excel"})
        with path.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); db=td/"m.db"; jobs=td/"jobs.csv"; out=td/"out.csv"; report=td/"report.json"
            self.make_postings(jobs); self.make_outcomes(out)
            self.run_cli("init","--db",db)
            self.run_cli("import-postings","--db",db,"--input",jobs,"--source","test")
            self.run_cli("import-outcomes","--db",db,"--input",out,"--cohort","test")
            self.run_cli("analyze","--db",db,"--title","Data Analyst","--location","Denver","--json","--out",report)
            data=json.loads(report.read_text())
            self.assertEqual(data["postings"]["n"],60)
            sql=next(x for x in data["postings"]["skills"] if x["skill"]=="SQL")
            self.assertAlmostEqual(sql["prevalence"],1.0)
            self.assertGreater(sql["lift"],5)
            assoc=next(x for x in data["outcomes"]["skills"] if x["skill"]=="SQL")
            self.assertGreater(assoc["risk_ratio"],2)

    def test_candidate_gap_not_claimed(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); db=td/"m.db"; jobs=td/"jobs.csv"; cand=td/"cand.json"; report=td/"report.json"
            self.make_postings(jobs)
            cand.write_text(json.dumps({"skills":["SQL","Python"]}),encoding="utf-8")
            self.run_cli("import-postings","--db",db,"--input",jobs,"--source","test")
            self.run_cli("analyze","--db",db,"--title","Data Analyst","--location","Denver","--candidate",cand,"--json","--out",report)
            data=json.loads(report.read_text())
            snow=next(x for x in data["candidate"]["comparison"] if x["skill"]=="Snowflake")
            self.assertEqual(snow["action"],"GAP / DO NOT CLAIM")
            self.assertFalse(snow["candidate_evidenced"])

    def test_sensitive_outcome_columns_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); db=td/"m.db"; f=td/"out.csv"
            with f.open("w",newline="",encoding="utf-8") as h:
                w=csv.DictWriter(h,fieldnames=["target_title","status","skills","race"]); w.writeheader(); w.writerow({"target_title":"Analyst","status":"hired","skills":"SQL","race":"x"})
            r=self.run_cli("import-outcomes","--db",db,"--input",f,"--cohort","test",check=False)
            self.assertNotEqual(r.returncode,0)
            self.assertIn("sensitive/protected-looking",r.stderr+r.stdout)

    def test_wage_column_not_false_positive_sensitive(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); db=td/"m.db"; f=td/"out.csv"
            with f.open("w",newline="",encoding="utf-8") as h:
                w=csv.DictWriter(h,fieldnames=["target_title","status","skills","wage"]); w.writeheader(); w.writerow({"target_title":"Analyst","status":"hired","skills":"SQL","wage":"80000"})
            r=self.run_cli("import-outcomes","--db",db,"--input",f,"--cohort","test",check=False)
            self.assertEqual(r.returncode,0,r.stderr+r.stdout)


    def test_onet_and_oews_imports(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); db=td/"m.db"; od=td/"onet"; od.mkdir(); report=td/"report.json"
            (od/"Occupation Data.csv").write_text("O*NET-SOC Code,Title\n15-2051.00,Data Scientists\n",encoding="utf-8")
            (od/"Essential Skills.csv").write_text("O*NET-SOC Code,Title,Element Name,Scale Name,Data Value\n15-2051.00,Data Scientists,Critical Thinking,Importance,4.1\n",encoding="utf-8")
            (od/"Software Skills.csv").write_text("O*NET-SOC Code,Title,Workplace Example,Hot Technology,In Demand\n15-2051.00,Data Scientists,Python,Y,Y\n",encoding="utf-8")
            self.run_cli("import-onet","--db",db,"--directory",od)
            oews=td/"oews.csv"
            oews.write_text("OCC_CODE,OCC_TITLE,AREA,AREA_TITLE,TOT_EMP,A_MEDIAN\n15-2051,Data Scientists,19740,Denver,1200,125000\n",encoding="utf-8")
            self.run_cli("import-oews","--db",db,"--input",oews,"--source-date","2025-05")
            self.run_cli("analyze","--db",db,"--title","Data Scientist","--location","Denver","--json","--out",report)
            data=json.loads(report.read_text())
            self.assertEqual(data["onet"]["code"],"15-2051.00")
            self.assertEqual(data["onet"]["software"][0]["name"],"Python")
            self.assertEqual(data["oews"][0]["annual_median"],125000)

if __name__=="__main__": unittest.main()
