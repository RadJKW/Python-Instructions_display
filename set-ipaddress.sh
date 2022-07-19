#!/bin/bash

# assign existing "static ip_address" for wlan0 interface to $ip_address from /etc/dhcpcd.conf
# ignore any "static ip_address=" that starts with "#"
# ignore any "static ip_address=" that is empty
#example ip_address = 10.11.18.50/16

get_ip_address() {
    #########################################################################################
    # Future: 
    #  - use this example: 
    ####   PS3="Enter a number: "
    ####   select character in Sheldon Leonard Penny Howard Raj
    ####   do
    ####      echo "Selected character: $character"
    ####      echo "Selected number: $REPLY"
    ####   done
    ####
    # change this function to grap all Static IP addresses from /etc/dhcpcd.conf
    # and ask the user to select one of them to change. 
    ########################################################################################## 

    
    # get the ipv4 address without the mask
    ip_address=$(cat /etc/dhcpcd.conf | grep "static ip_address=" | grep -v "^#" | grep -v "^$" | cut -d "=" -f 2 | cut -d "/" -f 1)
    # get the ipv4 mask
    ip_subnet=$(cat /etc/dhcpcd.conf | grep "static ip_address=" | grep -v "^#" | grep -v "^$" | cut -d "=" -f 2 | cut -d "/" -f 2)
    # display the full ipv4 address
    echo "Existing Static IP Address = $ip_address/$ip_subnet"
}

set_ip_address() {
    # Ask for new IP Address $new_ip_address
    read -p "Enter new IP Address: " new_ip_address

    # Ask for new IP Subnet $new_ip_subnet
    read -p "Enter new IP Subnet: " new_ip_subnet

}

get_hostname() {
    # get the hostname
    hostname=$(cat /etc/hostname)
    # display the hostname
    echo "Hostname = $hostname"
}

set_hostname() {
    # Ask for new hostname $new_hostname
    read -p "Enter new hostname: " new_hostname

}

apply_changes() {
    # Ask the user if they want to restart now
    # key 'y' for yes or 'n' for no
    read -p "Do you want to Apply Changes and restart now? (y/n): " restart_now
    # if the user wants to restart now
    if [ "$restart_now" = "y" ]; then
        # Replace existing "static ip_address" for wlan0 interface in /etc/dhcpcd.conf with new $ip_address
        sudo sed -i "s/static ip_address=$ip_address/static ip_address=$new_ip_address/g" /etc/dhcpcd.conf
        #Replace the subnet of the $new_ip_address with the $new_ip_subnet in /etc/dhcpcd.conf
        sudo sed -i "s/static ip_address=$new_ip_address\/$ip_subnet/static ip_address=$new_ip_address\/$new_ip_subnet/g" /etc/dhcpcd.conf
        # Display "New Wlan0 IP Address: $ip_address + "/" + $ip_subnet"
        echo "New Wlan0 IP Address: $new_ip_address/$new_ip_subnet"
        # restart dhcpcd to apply the changes
        echo "Restarting DHCP Client"
        sudo systemctl restart dhcpcd
        # display the new ipv4 address
        get_ip_address
        # Replace existing hostname in /etc/hosts & /etc/hostname with new $hostname
        sudo sed -i "s$hostname/$new_hostname/g" /etc/hosts
        sudo sed -i "s/$hostname/$new_hostname/g" /etc/hostname
        # Display "New Hostname: $hostname"
        echo "New Hostname: $new_hostname"
        # Inform the user " A restart is required to apply the new hostname"
        echo "A restart is required to apply the new hostname"

        # restart the system
        sudo reboot
    fi
}

get_hostname
set_hostname
get_ip_address
set_ip_address
apply_changes
