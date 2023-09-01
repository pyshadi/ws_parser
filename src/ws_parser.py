import pandas as pd
from scapy.all import *
from scapy.layers.http import HTTPRequest
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource, DataTable, TableColumn
import base64


class WiresharkParser:
    def __init__(self, pcapng_file):
        self.pcapng_file = pcapng_file
        self.df = pd.DataFrame(columns=['timestamp', 'src', 'dst', 'proto', 'length', 'sport', 'dport', 'payload'])

    def parse_packets(self):
        packets = rdpcap(self.pcapng_file)
        temp_df = pd.DataFrame(columns=['timestamp', 'src', 'dst', 'proto', 'length', 'sport', 'dport', 'payload'])
        for packet in packets:
            if IP in packet:
                timestamp = packet.time
                src = packet[IP].src
                dst = packet[IP].dst
                proto = packet[IP].proto
                length = packet[IP].len
                sport = packet[TCP].sport if TCP in packet else None
                dport = packet[TCP].dport if TCP in packet else None
                payload = None
                if Raw in packet:
                    if TCP in packet and packet[TCP].dport == 80:  # for HTTP traffic
                        try:
                            http_packet = HTTPRequest(packet[Raw])
                            payload = f"HTTP {http_packet.Method.decode()} {http_packet.Path.decode()}"
                        except Exception as e:
                            print(f"Couldn't parse HTTP payload: {e}")
                    else:  # for non-HTTP traffic
                        try:
                            payload = bytes(packet[Raw]).decode('utf-8')
                        except UnicodeDecodeError:
                            # Encode as base64
                            payload = base64.b64encode(bytes(packet[Raw])).decode('utf-8')
                temp_df = pd.concat([temp_df,
                                     pd.DataFrame([[timestamp, src, dst, proto, length, sport, dport, payload]],
                                                  columns=temp_df.columns)], ignore_index=True)
        self.df = pd.concat([self.df, temp_df], ignore_index=True)

    def visualize_network_traffic(self, plot_width=800, plot_height=400):
        source = ColumnDataSource(data=self.df)

        fig = figure(x_axis_type="datetime", plot_width=plot_width, plot_height=plot_height)
        fig.scatter(x='timestamp', y='length', source=source, color='blue')

        fig.xaxis.axis_label = 'Timestamp'
        fig.yaxis.axis_label = 'Packet Length'
        fig.title.text = 'Network Traffic'

        hover = HoverTool(
            tooltips=[
                ('Timestamp', '@timestamp'),
                ('Length', '@length'),
            ],
        )
        fig.add_tools(hover)

        show(fig)

    def visualize_network_traffic_table(self):
        source = ColumnDataSource(self.df)

        columns = [
            TableColumn(field='timestamp', title='Timestamp'),
            TableColumn(field='src', title='Source'),
            TableColumn(field='dst', title='Distination'),
            TableColumn(field='proto', title='Protocol'),
            TableColumn(field='length', title='Length'),
            TableColumn(field='sport', title='Source port'),
            TableColumn(field='dport', title='Distination port'),
            TableColumn(field='payload', title='Payload'),
        ]

        table = DataTable(source=source, columns=columns, width=1000, height=400)


        show(table)