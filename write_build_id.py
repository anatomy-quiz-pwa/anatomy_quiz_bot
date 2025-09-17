import datetime, subprocess, pathlib
ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
try:
    sha = subprocess.check_output(["git","rev-parse","--short","HEAD"]).decode().strip()
except Exception:
    sha = "no-git"
pathlib.Path(".build_id").write_text(f"{ts}-{sha}")
print("Wrote .build_id =", f"{ts}-{sha}")
