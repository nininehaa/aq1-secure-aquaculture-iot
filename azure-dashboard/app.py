from flask import Flask, jsonify, render_template, request
from datetime import datetime, timezone
import os,time,threading
app=Flask(__name__)
TOKEN=os.getenv("AQ1_DASHBOARD_TOKEN","")
OFFLINE=int(os.getenv("AQ1_OFFLINE_SECONDS","12"))
LOCK=threading.Lock(); EVENTS=[]; CONTROLLER={"state":"NORMAL","reason":"Waiting for verified telemetry","timestamp":None}
SENSORS={}
for pond in "ABC":
  for station in (1,2):
    for prefix,stype,unit in (("TEMP","temperature","C"),("DO","dissolved_oxygen","mg/L"),("PH","ph","pH")):
      sid=f"{prefix}-{pond}{station}"; SENSORS[sid]={"sensor_id":sid,"pond":pond,"station":f"{pond}{station}","sensor_type":stype,"value":None,"unit":unit,"verified":False,"last":None,"last_iso":None}
def now(): return datetime.now(timezone.utc).isoformat()
def auth(): return (not TOKEN) or request.headers.get("X-AQ1-Token","")==TOKEN
def event(kind,**kw):
  with LOCK:
    EVENTS.insert(0,{"kind":kind,"time":now(),**kw}); del EVENTS[100:]
@app.get("/")
def index(): return render_template("index.html")
@app.get("/health")
def health(): return jsonify(status="ok")
@app.get("/api/state")
def state():
  t=time.time()
  with LOCK:
    sensors=[]
    for s in SENSORS.values():
      x=dict(s); x["availability"]="ONLINE" if x["last"] and t-x["last"]<=OFFLINE else "OFFLINE"; sensors.append(x)
    return jsonify(sensors=sensors,controller=dict(CONTROLLER),events=list(EVENTS[:30]),offline_seconds=OFFLINE)
@app.post("/api/telemetry")
def telemetry():
  if not auth(): return jsonify(error="unauthorised"),401
  p=request.get_json(silent=True) or {}; sid=str(p.get("sensor_id","")).upper()
  if sid not in SENSORS: return jsonify(error="unknown sensor"),400
  if p.get("verified") is not True: return jsonify(error="verified telemetry only"),400
  s=SENSORS[sid]
  if p.get("sensor_type",s["sensor_type"])!=s["sensor_type"]: return jsonify(error="type mismatch"),400
  with LOCK:
    s.update(value=p.get("value"),unit=p.get("unit",s["unit"]),verified=True,last=time.time(),last_iso=now(),message_status=p.get("status","VERIFIED"),timestamp=p.get("timestamp"))
  event("VERIFIED_TELEMETRY",sensor_id=sid,value=p.get("value"),unit=p.get("unit",s["unit"]))
  return jsonify(accepted=True)
@app.post("/api/controller")
def controller():
  if not auth(): return jsonify(error="unauthorised"),401
  p=request.get_json(silent=True) or {}
  with LOCK: CONTROLLER.update(state=str(p.get("state","UNKNOWN")).upper(),reason=str(p.get("reason","")),timestamp=p.get("timestamp") or now())
  event("CONTROLLER",state=CONTROLLER["state"],reason=CONTROLLER["reason"]); return jsonify(accepted=True)
@app.post("/api/security-event")
def security_event():
  if not auth(): return jsonify(error="unauthorised"),401
  p=request.get_json(silent=True) or {}; event("SECURITY_EVENT",sensor_id=p.get("sensor_id"),event=p.get("event"),reason=p.get("reason")); return jsonify(accepted=True)
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","8000")))
