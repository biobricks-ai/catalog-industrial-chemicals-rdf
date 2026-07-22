import importlib.util,json
from pathlib import Path
import pyarrow.compute as pc
import pyarrow.parquet as pq
R=Path(__file__).parents[1];s=importlib.util.spec_from_file_location("v",R/"stages/validate_alias.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_exact_normalized_hashes():
 main,pmn=m.compare();assert main[0]==main[1]=="7e7c54868f3e44b4c37f80964e7c2253a1d203b660e0f6c054443ea8c3d79fc6";assert pmn[0]==pmn[1]=="47b8c9f53d0b1939b1faec5ac6e665909e1f6366cf541fa06035ed47e9a49e71"
def test_rows_and_coverage():
 c=json.loads((R/"health/source-coverage.json").read_text());assert c["tables_compared"]==c["tables_total"]==2 and c["rows_compared"]==c["source_rows"]==86862 and c["row_coverage"]==c["field_mapping_coverage"]==1
def test_n_hexane_in_both():
 for p,col in ((m.A/"tsca_inventory.parquet","CASRN"),(m.B/"tsca_inventory.parquet","casrn")):
  t=pq.read_table(p,columns=[col]);assert t.filter(pc.equal(t[col],"110-54-3")).num_rows==1
def test_alias_license_and_ontology():
 b=json.loads((R/"health/build-status.json").read_text());l=json.loads((R/"health/license.json").read_text());o=json.loads((R/"health/ontology-policy.json").read_text());assert b["status"]=="validated-alias" and b["graph_integration"] is False and not b["rdf_emitted"];assert l["status"]=="verified-consistent-public-domain-basis";assert o["alias_adds_classes"]==o["alias_adds_predicates"]==0
