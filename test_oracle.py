import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.environ["TNS_ADMIN"] = str(BASE_DIR / "core" / "db" / "wallet")
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_7")

conn = cx_Oracle.connect("ADMIN", "OracleCloud123", "lsy6fmm4lrc8s0kh_high")
print("Conectado correctamente!")
