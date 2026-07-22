#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
import pyarrow.parquet as pq
A=Path("/mnt/raid2/biobricks/catalog-industrial-chemicals-dataset-c/brick");B=Path("/mnt/raid2/biobricks/epa-tsca-inventory/brick")
def norm(x):
 if x is None:return ""
 if isinstance(x,float) and x.is_integer():return str(int(x))
 return str(x).strip()
def digest(cols):return hashlib.sha256("\n".join(sorted("\x1f".join(norm(x) for x in row) for row in zip(*cols))).encode()).hexdigest()
def compare():
 a=pq.read_table(A/"tsca_inventory.parquet").to_pydict();b=pq.read_table(B/"tsca_inventory.parquet").to_pydict();main=(digest([a[x] for x in ["CASRN","ChemName","ACTIVITY","FLAG","UVCB","DEF"]]),digest([b[x] for x in ["casrn","chemical_name","activity_status","flag","uvcb","definition"]]))
 a=pq.read_table(A/"pmn_accession.parquet").to_pydict();b=pq.read_table(B/"tsca_pmn_accession.parquet").to_pydict();pmn=(digest([a[x] for x in ["ID","PMNNO","ACCNO","UID","EXP","GenericName","FLAG","ACTIVITY"]]),digest([b[x] for x in ["id","pmnno","accno","uid","exp","genericname","flag","activity"]]))
 return main,pmn
if __name__=="__main__":
 main,pmn=compare();assert main[0]==main[1] and pmn[0]==pmn[1];print(json.dumps({"status":"validated no-output alias","main_hash":main[0],"pmn_hash":pmn[0]}))
