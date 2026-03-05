param(
  [Parameter(Mandatory=$true)]
  [string]$Host,

  [int]$Port = 1883,

  [string]$Topic = "dams/sim/telemetry"
)

# Passive 30s
python mqtt_sim.py --host $Host --port $Port --topic $Topic --mode passive --seconds 30

# Active burst 10s
python mqtt_sim.py --host $Host --port $Port --topic $Topic --mode active --seconds 10

# Passive 30s
python mqtt_sim.py --host $Host --port $Port --topic $Topic --mode passive --seconds 30
