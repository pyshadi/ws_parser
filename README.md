# Wireshark Packet Parser and Visualizer
The Wireshark packet parser and visualizer extracts information from .pcapng files and visualizes network traffic data.

## Dependencies
You need to have the following libraries:

* pandas
* scapy
* scapy-http
* bokeh

## Usage
1- Create an instance of the <code>WiresharkParser</code> class by providing the path to your .pcapng file as a string. <br>
2- Use the <code>parse_packets</code> method to parse the packets from the pcapng file, and the <code>visualize_network_traffic</code> and <code>visualize_network_traffic_table</code> methods to visualize the network traffic data.

```
from wireshark_parser import WiresharkParser

# Create an instance of the WiresharkParser class
parser = WiresharkParser("path/to/your/file.pcapng")

# Parse the packets
parser.parse_packets()

# Visualize the network traffic
parser.visualize_network_traffic()

# Visualize the network traffic in a table
parser.visualize_network_traffic_table()
```
The visualizations include a scatter plot of packet lengths over time and a table of the packet data.