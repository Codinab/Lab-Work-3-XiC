SNMP Data analyzer for Lab Work 3
==============================

<div align="center">
  <a href="https://drive.google.com/uc?export=view&id=1ftl2blHrrtjk3r1kaECPOjPa8LrpX2FI"><img src="https://drive.google.com/uc?export=view&id=1ftl2blHrrtjk3r1kaECPOjPa8LrpX2FI" style="width: 650px; max-width: 100%; height: auto" title="SNMP Data Analyzer Logo" /a>
</div>

# Introduction
This project contains the code and resources necessary to implement an SNMP data analysis tool that was used in "Xarxes i Comunicacions" subject in [Computer Science Engineering](https://grauinformatica.udl.cat/en) at [Universitat de Lleida (UdL)](https://www.udl.cat/ca/en/).

# Project Idea
The SNMP Data Analyzer project aims to provide a comprehensive tool for managing and monitoring networks using the Simple Network Management Protocol (SNMP). The goal is to develop a user-friendly application that simplifies the process of gathering and analyzing SNMP data from network devices.

The project encompasses various functionalities, including device discovery, real-time monitoring, and alerting mechanisms. By leveraging SNMP, the application enables administrators to efficiently monitor critical network parameters such as CPU load, memory usage, interface status, and more.

The SNMP Data Analyzer provides a centralized platform for visualizing network data, generating reports, and setting up customized alert thresholds. The intuitive user interface allows users to easily navigate through the network topology and obtain insights into device performance and network health.

## Objectives

The objectives of the SNMP Network Management Application are as follows:

1. **Polling all the routers**: Retrieve the sysName and IP information of all the routers in the network using SNMP. This information includes the IP address, netmask, speed, and status of the interfaces. Consider using the net-snmp Python bindings and OSPF-MIBs to discover the neighbors.

2. **Getting the routing tables**: Retrieve the routing table of each router. The routing table should include the network, netmask, next hop, and route type. Consider using the ipCidrRouteTable from the IP-FORWARD-MIB.

3. **Creating route summaries**: Create route summaries between every pair of IP addresses in the network. For each possible IP pair, calculate the shortest path using the sysNames of the routers. Mask the IP addresses using the python-netaddr library.

4. **Plotting the network**: Generate a graphical representation of the network architecture in a readable format, such as DOT or PDF. Label each node with its sysName and each link with the peer IP addresses and link speed. Consider using Graphviz to create the network visualization.

5. **Monitoring the network**: Send SNMP traps from the routers to monitor the network. Use Cisco traps for OSPF state changes and neighbor state changes (CISCO ospfstate-change and neighbor-state-change). Receive and process the traps using snmptrapd. Print and decode all the trap information.

# Project Setup Instructions

To install the project and all its dependencies easily, a requirements.txt file has been provided. Follow the steps below to install these dependencies:

1. Ensure that Python is installed on your system.
2. Clone this repository onto your local machine.

    ```
    pip install -r requirements.txt
    ```

3. Navigate to the project directory.
4. Open a terminal and execute the following command to install the dependencies:

    ```
    pip install -r requirements.txt
    ```

# Tool Usage Guide

In this section, you will find a variety of examples that demonstrate the practical application of the python-snmp-analyzer tool. Prior to running the tool, it is important to ensure that all the necessary dependencies have been successfully installed.

## Executing the tool with default settings
To initiate the tool using the default configurations, execute the command provided below:
```shell
python3 main.py
```

## Command-line Options
The program supports the following command-line options:

- `--router-ip`: Specifies the IP address of the router you want to connect to.

  Example:
  ```shell
  python3 main.py --router-ip 10.0.0.3
  ```
  
- `--community-string`: Sets the community string to be used for authentication.

  Example:
  ```shell
  python3 main.py --community-string rocom 
  ```
  
- `--print-networks`: Prints a list of networks available on the router.

  Example: 
  ```shell
  python3 main.py --print-networks
  ```


- `--print-routers`: Displays information about the connected routers.

  Example: 
  ```shell
  python3 main.py --print-routers
  ```

- `--create-network-graph`: Generates a graphical representation of the network.

  Example: 
  ```shell
  python3 main.py --create-network-graph
  ```

- `--graph-file`: Specifies the name of the file to save the network graph (default: network_map).

  Example: 
  ```shell
  python3 main.py --graph-file [my_network_graph_file]
  ```

You can replace `[my_network_graph_file]` with the desired name for the network graph file.

# Tool Usage Guide

Certainly! Here's the information provided in a README.md format:

# Trap Catcher Setup

To set up the trap catcher and parse SNMP traps, follow the steps below:

## Configuration Steps

1. Navigate to the `traps` directory:

   ```shell
   cd traps
   ```

3. Copy the trap configuration and parser files:

   ```shell
   # Copy configuration files
   sudo cp snmptrapd.conf /etc/snmp
   sudo cp snmpd.conf /usr/share/snmp

   # Create directory for parser files
   sudo mkdir /etc/snmp/scripts
   sudo cp traps_parser /etc/snmp/scripts
   ```

5. Start the SNMP services:
   ```shell
   sudo systemctl start snmpd
   sudo systemctl start snmptrapd
   ```

6. (Optional) Provide executable permissions to the traps_parser script if necessary:
   ```shell
   cd /etc/snmp/scripts
   sudo chmod +x traps_parser
   ```

## Viewing Parsed Traps

To view the parsed traps, perform the following steps:

1. Check the output and view the traps information in the `/tmp/log` file.

   Example Output:
   ```
   Trap: 
  
   Host: <UNKNOWN>
  
   IP: UDP: [11.0.0.2]:65447->[10.0.0.3]:162
  
   Variables:
   SNMPv2-MIB::sysUpTime.0 = 0:0:18:26.33
   SNMPv2-MIB::snmpTrapOID.0 = OSPF-MIB::ospf.16.2.2
   OSPF-MIB::ospfRouterId.OSPF-MIB::ospfRouterId = 12.0.0.1
   OSPF-MIB::ospfNbrIpAddr.OSPF-MIB::ospfNbrIpAddr = 12.0.0.2
   OSPF-MIB::ospfNbrAddressLessIndex.OSPF-MIB::ospfNbrAddressLessIndex = 0
   OSPF-MIB::ospfNbrRtrId.OSPF-MIB::ospfNbrRtrId = 12.0.0.2
   OSPF-MIB::ospfNbrState.OSPF-MIB::ospfNbrState = full
  
  
   Trap: 
  
   Host: <UNKNOWN>
  
   IP: UDP: [10.0.0.2]:51107->[10.0.0.3]:162
  
   Variables:
   SNMPv2-MIB::sysUpTime.0 = 0:0:00:12.11
   SNMPv2-MIB::snmpTrapOID.0 = OSPF-MIB::ospf.16.2.2
   OSPF-MIB::ospfRouterId.OSPF-MIB::ospfRouterId = 13.0.0.1
   OSPF-MIB::ospfNbrIpAddr.OSPF-MIB::ospfNbrIpAddr = 11.0.0.2
   OSPF-MIB::ospfNbrAddressLessIndex.OSPF-MIB::ospfNbrAddressLessIndex = 0
   OSPF-MIB::ospfNbrRtrId.OSPF-MIB::ospfNbrRtrId = 12.0.0.1
   OSPF-MIB::ospfNbrState.OSPF-MIB::ospfNbrState = twoWay
   ```
   
   The parsed traps will be displayed in a structured format, showing relevant information such as router ID, interface ID, and interface state.

Please note that the `/tmp/log` file will contain the output with the parsed traps information.


# Authors

* [Àlex Codina Braceros](https://github.com/Codinab)
* [Mario Fernández Rodríguez](https://github.com/marioferro2002)
* [Pol Triquell Lombardo](https://github.com/poltriquell)

# License
The project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more information.
