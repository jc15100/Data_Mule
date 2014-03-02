#!/usr/bin/perl -w

# Make sure SD-Card is connected
$media_name = "mmcblk0p1";
$sd_check = "ls /media/ | grep ".$media_name;
@ret = `$sd_check`;
$size = @ret;
if ($size == 0) {
   print "\nFAILED: Did not found SD-Card!\n";	
   exit 1;
}
print "\nOK: Found SD-Card!\n";

# Make sure directory structure is in place
if (-l "~/mule_data"){
  print "\nOK: Found data directory!\n";
}
else{
  print "\nOK: Data directory not found. Creating data directory\n"; 
  
  if(-d "/media/".$media_name."/mule_data/"){
      print "\nOK: Data directory found in SD-Card!";	
  }
  else{
      `mkdir /media/$media_name/mule_data/`;
      print "\nOK: Creating link to data directory!";
  }
  `ln -s /media/$media_name/mule_data/ ~/mule_data`;
}

# Setup ad-hoc network
$ip_addr = "192.168.1.2";
`ifconfig wlan0 up`;
`iwconfig wlan0 mode ad-hoc`;
`iwconfig wlan0 essid "mule"`;
`ifconfig wlan0 $ip_addr netmask 255.255.255.0`;

#`iwconfig > tmp.txt`;
#`cat tmp.txt | grep ESSID | sed 's/.*ESSID.\(.*\)/\1/g'`;

