param(
  [Parameter(Mandatory=$true)]
  [string]$Iface
)

# Passive 30s
python ssdp_sim.py --iface $Iface --mode passive --seconds 30 --passive-interval 10

# Active burst 10s
python ssdp_sim.py --iface $Iface --mode active --seconds 10 --active-burst-size 30 --active-interval 2 --active-burst-gap 0.05

# Passive 30s
python ssdp_sim.py --iface $Iface --mode passive --seconds 30 --passive-interval 10