# CAN Decoder
A Tritium-formatted CAN log decoder written in Python

## Usage Instructions

```
usage: canDecode.py [-h] [--dbc DBC [DBC ...]] [--filter FILTER [FILTER ...]] [--unknown] [--all] logs [logs ...]

--dbc        the DBC file(s) to decode the CAN log
--filter    the CAN ID(s) to filter while decoding
--unknown    logs only unknown messages
--all        logs all packets, including unknown messages
logs        the CAN log(s) to decode
```

### Example

This example decodes a Tritium-formatted CAN log CSV file using CAN database container (DBC) files. It will decode CAN packets from the:
Tritium battery management system (BMS)
Elmar maximum power point tracker (MPPT)
Tritium motor controller (WaveSculptor22)

```
canDecode.exe 'canlog_yyyy-mm-dd_hh-mm-ss.csv' --dbc tritium_bms_bmu.dbc elmar_mppt_a.dbc elmar_mppt_b.dbc elmar_mppt_c.dbc wavesculptor22_left.dbc wavesculptor22_right.dbc
```

## Credits

A special thanks to Karl Ding for their contributions to the solar car and open source community with the original [WaveSculptor22 DBC file](https://github.com/karlding/wavesculptor-22-dbc) and [incredibly helpful guides](https://justkding.me/thoughts/decoding-can-with-dbc-files).