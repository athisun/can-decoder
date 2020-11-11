#!/usr/bin/env python3
#
# > python3 canDecode.py canlog_2019-08-17_12-03-55 (stop test).csv --dbc .\dist\wavesculptor22_left.dbc
# Message: {'Temperature': 250.1, 'AverageRadius': 3.2, 'Enable': 'Enabled'}
# Encoded: c001400000000000
# Decoded: {'Enable': 'Enabled', 'AverageRadius': 3.2, 'Temperature': 250.1}
#

import argparse
from binascii import unhexlify
import cantools
import csv
import os

# Read in the command line args
parser = argparse.ArgumentParser(description='Decode a Tritium CAN log.')
parser.add_argument('--dbc', nargs='+',
                   help='the DBC file(s) to decode the CAN log')
parser.add_argument('--filter', nargs='+',
                   help='the CAN ID(s) to filter while decoding')
parser.add_argument('--unknown', action='store_true',
                   help='logs only unknown messages')
parser.add_argument('--all', action='store_true',
                   help='logs all packets, including unknown messages')
parser.add_argument('logs', nargs='+',
                   help='the CAN log(s) to decode')
args = parser.parse_args()

# Create database from DBC file(s)
database = cantools.db.Database()
for dbc in args.dbc:
    database.add_dbc_file(dbc)

# Specify the Tritium CAN log CSV column headers
recvTimeIdx, packetNumIdx, canIdIdx, flagsIdx, dataIdx, float1Idx, float0Idx, senderAddrIdx = range(0, 8)
known_can_ids = list(message.frame_id for message in database.messages)

# Read in logs(s) from command line args
for log in args.logs:
    filename = os.path.splitext(log)[0]
    with open(filename + '_decoded.csv', mode='w', newline='') as decoded_file:
        csv_writer = csv.writer(decoded_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        with open(log, newline='') as csvFile:
            canLog = csv.reader(csvFile, delimiter=',')
            next(canLog) # Skip the header row

            for packet in canLog:
                # Get the CAN ID
                can_id_str = packet[canIdIdx].strip() # Remove whitespace
                can_id = int(can_id_str[2:], 16) # Remove '0x' and parse as integer

                timestamp = packet[recvTimeIdx].strip() # Remove whitespace

                # Skip decoding this packet if it's not in the database
                if (can_id not in known_can_ids):
                    if (args.all or args.unknown):
                        print(timestamp, can_id_str, 'Unknown packet')
                    continue

                # Skip decoding this packet if we only want unknown packets
                if (args.unknown and not args.all):
                    continue

                # Skip decoding this packet if it's not in our filter
                if (args.filter and can_id_str[2:] not in args.filter):
                    continue

                # Decode the packet
                msg = database.get_message_by_frame_id(can_id)
                data_str = packet[dataIdx].strip()[2:] # Remove whitespace and '0x'
                data_bin = unhexlify(data_str)[::-1] # Hex to binary, reverse binary
                data = database.decode_message(can_id, data_bin)
                # cycle_time_hz = str(round(1000/msg.cycle_time))+'Hz'

                # Write a line for every data point
                for key, value in data.items():
                    csvData = [timestamp, can_id_str, msg.name, key, value]
                    csv_writer.writerow(csvData)