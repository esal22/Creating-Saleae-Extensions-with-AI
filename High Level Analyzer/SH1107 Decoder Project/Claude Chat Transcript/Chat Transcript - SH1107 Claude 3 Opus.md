# Claude 3 Opus Chat Transcript
This is the chat transcript for this experiment.


# Begin Chat Transcript

## Attachments
    - SH1107.pdf    <- Datasheet PDF
    - Saleae Support.pdf    <- Export of Support Articles to PDF
    - HighLevelAnalyzer.py  <- HLA Reference Design Python File


## Prompt Text User Input 1
    What steps are needed to decode the I2C frames used to communicate between a microcontroller and the SH1107?


## Claude Response 1
Based on the SH1107 datasheet, here are the key steps to decode the I2C frames used to communicate between a microcontroller and the SH1107 OLED controller:

1. Identify the I2C slave address of the SH1107. It uses two 7-bit slave addresses - 0111100 and 0111101. The least significant bit is determined by the SA0 pin.

2. The first byte after the slave address determines if the following bytes are command or display data:
- If the first byte is 0x00, the following bytes are interpreted as command bytes
- If the first byte is 0x40, the following bytes are interpreted as display data bytes

3. If the bytes are command bytes, they need to be decoded based on the SH1107 command set in the datasheet. Key commands include:
- Set Lower/Higher Column Address 
- Set Memory Addressing Mode
- Set Contrast Control
- Set Segment Re-map  
- Set Display ON/OFF
- Set Page Address

4. If the bytes are display data bytes, they represent the actual pixel data to turn on/off pixels in the OLED display. The datasheet explains the memory mapping between the display data bytes and the OLED segments/commons.

5. Use the memory addressing mode (page or vertical) to determine how to interpret the sequence of data bytes.

6. Continue decoding the I2C frames as commands or data based on the first byte after the slave address in each new frame.

So in summary, the key is to track whether each I2C frame is sending a command or display data, decode the commands into human-readable form using the SH1107 command table, and map the data appropriately to the OLED display memory based on the configured memory addressing mode. The datasheet has the complete command reference and memory mapping details needed for the decoding.


## Prompt Text User Input 2
modify the HighLevelAnalyser.py to decode incoming I2C frames for the SH1107 using the Saleae Support.pdf as reference as well as the attached datasheet. Each frame should have a human readable discription of the byte above the byte value in Logic2.


## Claude Response 2
Here's the modified HighLevelAnalyzer.py to decode incoming I2C frames for the SH1107 based on the provided datasheet:

```python
from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

class Hla(HighLevelAnalyzer):
    result_types = {
        'sh1107': {
            'format': '{{data.description}}'
        }
    }

    commands = {
        0x81: {'name': 'Contrast Control Mode Set', 'params': 1},
        0xAE: {'name': 'Display OFF', 'params': 0},
        0xD5: {'name': 'Set Display Clock Divide Ratio/Oscillator Frequency', 'params': 1},
        0x20: {'name': 'Set Memory Addressing Mode', 'params': 1},
        0xAD: {'name': 'DC-DC Control Mode Set', 'params': 1},
        0xA0: {'name': 'Set Segment Re-map', 'params': 1},
        0xC0: {'name': 'Set COM Output Scan Direction', 'params': 1},
        0xDC: {'name': 'Set Display Start Line', 'params': 1},
        0xD3: {'name': 'Set Display Offset', 'params': 1},
        0xD9: {'name': 'Set Pre-charge Period', 'params': 1},
        0xDB: {'name': 'Set VCOMH Deselect Level', 'params': 1},
        0xA8: {'name': 'Set Multiplex Ratio', 'params': 1},
        0xA4: {'name': 'Entire Display ON', 'params': 0},
        0xA6: {'name': 'Set Normal/Inverse Display', 'params': 0}
    }

    def __init__(self):
        self.state = 'ADDRESS'
        self.transaction_type = None
        self.cmd_params = []

    def decode(self, frame):
        if frame.type == 'address':
            self.state = 'ADDRESS'
            address = frame.data['address'][0]
            if address == 0x3C:  # SH1107 I2C address
                return AnalyzerFrame('sh1107', frame.start_time, frame.end_time, {'description': f'Address: 0x{address:02X}'})
        elif frame.type == 'data':
            data = frame.data['data'][0]
            if self.state == 'ADDRESS':
                self.transaction_type = 'COMMAND' if data == 0x00 else 'DATA'
                self.state = self.transaction_type
                return AnalyzerFrame('sh1107', frame.start_time, frame.end_time, {'description': f'Transaction Type: {self.transaction_type}'})
            elif self.state == 'COMMAND':
                if data in self.commands:
                    command = self.commands[data]
                    self.cmd_params = [data]  # Store the command byte as the first parameter
                    if command['params'] > 0:
                        self.state = 'COMMAND_PARAMS'
                    else:
                        self.state = 'COMMAND'
                    return AnalyzerFrame('sh1107', frame.start_time, frame.end_time, {'description': f'Command: {command["name"]}'})
                else:
                    self.state = 'COMMAND'
                    return AnalyzerFrame('sh1107', frame.start_time, frame.end_time, {'description': f'Unknown Command: 0x{data:02X}'})
            elif self.state == 'COMMAND_PARAMS':
                self.cmd_params.append(data)
                if self.cmd_params[0] in self.commands and len(self.cmd_params) - 1 == self.commands[self.cmd_params[0]]['params']:
                    param_str = ' '.join([f'0x{p:02X}' for p in self.cmd_params[1:]])
                    self.state = 'COMMAND'
                    return AnalyzerFrame('sh1107', frame.start_time, frame.end_time, {'description': f'Command Params: {param_str}'})
            elif self.state == 'DATA':
                return AnalyzerFrame('sh1107', frame.start_time, frame.end_time, {'description': f'Data: 0x{data:02X}'})
```

This HLA does the following:

1. It defines a dictionary `commands` that maps command bytes to their names and the number of parameter bytes they expect.

2. In the `decode` method, it first checks if the frame is an address frame. If it matches the SH1107 I2C address (0x3C), it outputs an address frame.

3. If the frame is a data frame, it checks the current state:
   - If the state is 'ADDRESS', it determines if the first data byte is a command (0x00) or data (0x40) and updates the state accordingly.
   - If the state is 'COMMAND', it checks if the data byte matches a known command. If so, it outputs a command frame and updates the state to collect command parameters if necessary. If the command is unknown, it outputs an unknown command frame.
   - If the state is 'COMMAND_PARAMS', it collects the parameter bytes until it has the expected number for the current command, then outputs a command parameter frame.
   - If the state is 'DATA', it simply outputs a data frame.

4. The result is that each I2C frame will have a human-readable description above the byte value in the Logic 2 software, indicating whether it is an address, command, command parameter, or display data byte.

Note: Make sure to replace the existing `HighLevelAnalyzer.py` file in your extension folder with this modified version.


# End Chat Transcript

# Next Step
## Test Out the Modified HighLevelAnalyzer.py
- Copy and paste the python code above into the `HighLevelAnalyzer.py` file.
- Save and load the new HLA in the Saleae Logic 2 software.


