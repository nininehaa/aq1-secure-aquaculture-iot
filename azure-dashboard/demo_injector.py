import random,time
from datetime import datetime,timezone
from azure_sender import send_verified_telemetry,send_controller_state
def now(): return datetime.now(timezone.utc).isoformat()
R={"TEMP":(23.5,25.5,"temperature","C"),"DO":(6.8,7.8,"dissolved_oxygen","mg/L"),"PH":(7.2,7.8,"ph","pH")}
send_controller_state("NORMAL","Verified telemetry available",now())
print("Sending AQ-1 demo telemetry to Azure; Ctrl+C to stop")
while True:
  for p in "ABC":
    for st in (1,2):
      for pre,(lo,hi,typ,u) in R.items(): send_verified_telemetry({"sensor_id":f"{pre}-{p}{st}","sensor_type":typ,"value":round(random.uniform(lo,hi),2),"unit":u,"status":"VERIFIED","timestamp":now()})
  time.sleep(5)
