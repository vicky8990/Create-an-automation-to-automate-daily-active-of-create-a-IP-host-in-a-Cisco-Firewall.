# Create-an-automation-to-automate-daily-active-of-create-a-IP-host-in-a-Cisco-Firewall.
Automation the process of create an IP HOST which I have to block in my Cisco Firewalls.

#Information 

This script automates the process of adding network objects and groups to Cisco Firepower Device Manager (FDM) using its REST API. Instead of manually creating each network (IP) object and grouping them through the FDM web interface, this tool reads a list of IP addresses from a file (ip.txt) and programmatically creates the corresponding network objects in FDM. After all objects are created, the script can also group these IP objects into a single network group, making it easier to manage firewall rules and policies.

This approach saves time, reduces manual errors, and is especially useful when dealing with large numbers of IP addresses that need to be blocked, allowed, or otherwise managed as a group within the firewall system.

-The main file is the script file which receive data from USER End.
   #fdm_object_adder.py is the main file 

-And the file where you can enter the input of IP's and URL's 
   #ip.txt and #url.txt

#How to run the code or clone. 
   

