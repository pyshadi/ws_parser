from ws_parser import  WiresharkParser


parser = WiresharkParser(r'..\data\capture')
parser.parse_packets()
parser.visualize_network_traffic()
parser.visualize_network_traffic_table()