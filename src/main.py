from ws_parser import  WiresharkParser


parser = WiresharkParser(r'C:\Users\soundation\source\ws_parser\data\capture')
parser.parse_packets()
parser.visualize_network_traffic()
parser.visualize_network_traffic_table()