sudo tunctl -t tap0 -u "$USER"
sudo ip link set tap0 up
sudo ip addr add 10.0.0.3/8 dev tap0
sudo ip route add 12.0.0.0/8 via 10.0.0.2 dev tap0
sudo ip route add 11.0.0.0/8 via 10.0.0.2 dev tap0
sudo ip route add 13.0.0.0/8 via 10.0.0.2 dev tap0