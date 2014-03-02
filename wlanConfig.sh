if [ -z "$1" ]; then
	echo 'Please specify last octet of IP as argument. Exiting..'
	exit
fi
iwconfig wlan0 up
iwconfig wlan0 mode ad-hoc
iwconfig wlan0 essid "mule"    
ifconfig wlan0 192.168.1.$ip netmask 255.255.255.0

