# CVP L3 Leaf Spine Configlet Builder
This set of scripts are a basis on building the configurations for a layer 3 leaf and spine topology.  These scripts will only configure interfaces and BGP settings for each device.

This configlet builder will work on devices newly joined to CloudVision.  Within the l3ls.yml file, there is a section that ties the system MAC Addresses for the switches to their hostnames.

### Setup
Few notes on the configuration of the l3ls.yml file:

This file will be installed in the following directory on the CloudVision appliance:
	/home/cvp/hostvars/l3ls.yml

When mapping system MAC addresses to hostnames, this will be done in the devices section:

	devices:
 		2c:c2:60:56:df:93: spine1

The flow of the remainder of the YAML file for the configuration is as follows:

	topology:
		spine1: <-- This needs to be the same as the hostname specified in the 'devices' mapping
			interfaces:
				ethernet: <-- Section where all the interfaces on the switch will be specified.
					Ethernet1: <-- Interface name needs to be this format for the switches configuration
				loopback:
					...
				...
			BGP:
				bgp_neighbors: <-- Starts the mapping for bgp neighbors
					- - leaf1 <-- hostname of the BGP neighbor device
					  - Ethernet2 <-- Interface on the BGP neighbor device

### Topology
Here is a high level overview for the interface connections between each Spine and Leaf.

Format for the connections:  [Device][Interface] <---> [Device][Interface]
- [spine1][Ethernet1] <--> [spine2][Ethernet1]
- [spine1][Ethernet2] <--> [leaf1][Ethernet2]
- [spine1][Ethernet3] <--> [leaf2][Ethernet2]
- [spine1][Ethernet4] <--> [leaf3][Ethernet2]
- [spine1][Ethernet5] <--> [leaf4][Ethernet2]
- [spine1][Ethernet6] <--> [leaf5][Ethernet2]
- [spine1][Ethernet7] <--> [leaf6][Ethernet2]
- [spine2][Ethernet2] <--> [leaf1][Ethernet3]
- [spine2][Ethernet3] <--> [leaf2][Ethernet3]
- [spine2][Ethernet4] <--> [leaf3][Ethernet3]
- [spine2][Ethernet5] <--> [leaf4][Ethernet3]
- [spine2][Ethernet6] <--> [leaf5][Ethernet3]
- [spine2][Ethernet7] <--> [leaf6][Ethernet3]
- [leaf1][Ethernet1] <--> [leaf2][Ethernet1]
- [leaf3][Ethernet1] <--> [leaf4][Ethernet1]
- [leaf1/2/3/4][Ethernet4/5] <--> [host_devices]




### Future Releases
Here are some of the future additions to this CVP topology builder:
- Separate out the L3 interface configurations from the BGP configurations into separate configlet builders
- Add support for specifying networks to be advertised via BGP
- Overlay support
- Streamline process for generating the YAML file