 Wi-Fi Network Scanner

A simple, beginner-friendly Python program that finds all the devices connected to your Wi-Fi network -your phone, laptop, smart TV, router, and more.

When you run it on your laptop, it shows you every other device on the same Wi-Fi, including their IP address,MAC address,vendor(Apple, Samsung, TP-Link…), and hostname.


## Features

Lists every active device on your Wi-Fi network
Shows each device's IP address
Shows each device's MAC address
Guesses the vendor/maker from the MAC address
Shows the device hostname when available
pings all addresses at the same time
Simple, single file, fully commented 
No admin rights needed and no scapy required
Works on Windows, Linux, and macOS

##  Requirements

Python 3.8 or newer
(Optional) the `mac-vendor-lookup` package, to show device vendors


##  Installation


# 1. Download / clone this project
git clone https://github.com/nipunashadow-ui/wifi-scanner.git
cd wifi-scanner

# 2. (Optional but recommended) install the vendor-lookup package
pip install -r requirements.txt



## How to Run

Make sure your computer is connected to the Wi-Fi you want to scan, then run on terminal:

python wifi_scanner.py



## Example Output

======================================================================
 Wi-Fi Network Scanner
 Only scan networks you own or are allowed to use!
======================================================================
[*] My IP address : 192.168.1.5
[*] Pinging 254 addresses, please wait...
[*] Found 4 device(s) on the network.

IP Address       MAC Address          Vendor                 Hostname
--------------------------------------------------------------------------------
192.168.1.1      a4:b1:c2:d3:e4:f5    TP-Link Technologies   router.local
192.168.1.5      11:22:33:44:55:66    Intel Corporate        my-laptop      
192.168.1.12     aa:bb:cc:dd:ee:ff    Apple, Inc.            iphone.local
192.168.1.20     99:88:77:66:55:44    Samsung Electronics    galaxy-tab
---------------------------------------------------------------------------------

## How It Works (simple explanation)

1. Find my own IP -e.g. `192.168.1.5`.
2. Work out the network range -e.g. `192.168.1.1` to `192.168.1.254`.
3. Ping every address - so the devices reply and the operating system records their MAC addresses.
4. Read the ARP table - the list the OS keeps of which device (MAC) is at which IP and print it nicely.


## Troubleshooting


If Vendors column is empty - Run `pip install mac-vendor-lookup` 
A device is missing , It may be asleep or have a firewall. Wake it and run again. 
First vendor lookup is slow , It downloads a vendor database once, then it's cached. 

## Problems

If have enabled MAC Address randomaization in Host devices, shown a defferent randomized MAC addresses in this programm(Modern devices have this feature from prevent tracking them by third parties)

## What I Learned Building This

- Working with the Python standard library (`socket`, `subprocess`, `ipaddress`, `re`)
- Running tasks in parallel with `ThreadPoolExecutor`
- Parsing command output with regular expressions
- Writing clean, well-commented, readable code

