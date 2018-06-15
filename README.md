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

### Future Releases
Here are some of the future additions to this CVP topology builder:
- Separate out the L3 interface configurations from the BGP configurations into separate configlet builders
- Add support for specifying networks to be advertised via BGP
- Overlay support