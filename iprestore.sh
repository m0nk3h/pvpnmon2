name="$1/iptables.backup"
iptables -F
iptables-restore < $name
