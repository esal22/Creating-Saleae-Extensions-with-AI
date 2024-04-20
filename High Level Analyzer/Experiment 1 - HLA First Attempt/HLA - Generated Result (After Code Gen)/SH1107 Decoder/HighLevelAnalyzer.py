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