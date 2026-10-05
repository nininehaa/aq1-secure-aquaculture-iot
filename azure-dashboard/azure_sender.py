import json,os,urllib.request,urllib.error
BASE=os.getenv("AQ1_AZURE_DASHBOARD_URL","").rstrip("/"); TOKEN=os.getenv("AQ1_DASHBOARD_TOKEN","")
def _post(path,payload,timeout=4):
  if not BASE: return False
  h={"Content-Type":"application/json"}
  if TOKEN: h["X-AQ1-Token"]=TOKEN
  req=urllib.request.Request(BASE+path,data=json.dumps(payload).encode(),headers=h,method="POST")
  try:
    with urllib.request.urlopen(req,timeout=timeout) as r: return 200<=r.status<300
  except Exception: return False
def send_verified_telemetry(payload):
  p=dict(payload); p["verified"]=True; return _post("/api/telemetry",p)
def send_controller_state(state,reason,timestamp=None): return _post("/api/controller",{"state":state,"reason":reason,"timestamp":timestamp})
def send_security_event(event,sensor_id=None,reason=None): return _post("/api/security-event",{"event":event,"sensor_id":sensor_id,"reason":reason})
