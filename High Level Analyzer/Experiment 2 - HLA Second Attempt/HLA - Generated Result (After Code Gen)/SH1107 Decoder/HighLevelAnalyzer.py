# High Level Analyzer for SH1107 OLED display driver
# For more information and documentation, please go to https://support.saleae.com/extensions/high-level-analyzer-extensions

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

# Define instruction set lookup table
INSTRUCTIONS = {
    0x00: {"name": "Set Lower Column Address", "description": "Sets 4 lower bits of column address of display RAM", "params": 1},
    0x10: {"name": "Set Higher Column Address", "description": "Sets 4 higher bits of column address of display RAM", "params": 1},
    0x20: {"name": "Set Memory Addressing Mode", "description": "Sets the memory addressing mode", "params": 1},
    0x81: {"name": "Set Contrast Control", "description": "Sets the contrast setting of the display", "params": 1},
    0x8D: {"name": "Charge Pump Setting", "description": "Enable/disable charge pump", "params": 1},
    0xA0: {"name": "Set Segment Re-map", "description": "Set segment re-map", "params": 1},
    0xA8: {"name": "Set Multiplex Ratio", "description": "Set multiplex ratio", "params": 1},
    0xAE: {"name": "Display OFF", "description": "Turns the display off", "params": 0},
    0xAF: {"name": "Display ON", "description": "Turns the display on", "params": 0},
    0xD3: {"name": "Set Display Offset", "description": "Set display offset", "params": 1},
    0xD5: {"name": "Set Display Clock Divide Ratio/Oscillator Frequency", "description": "Set display clock divide ratio/oscillator frequency", "params": 1},
    0xD9: {"name": "Set Pre-charge Period", "description": "Set pre-charge period", "params": 1},
    0xDA: {"name": "Set COM Pins Hardware Configuration", "description": "Set COM pins hardware configuration", "params": 1},
    0xDB: {"name": "Set VCOMH Deselect Level", "description": "Set VCOMH deselect level", "params": 1},
    0xB0: {"name": "Set Page Address", "description": "Set GDDRAM page start address for page addressing mode", "params": 1}
}

class Hla(HighLevelAnalyzer):
    result_types = {
        'address': {
            'format': 'Device Address: {{data.address}}, {{data.rw}}'
        },
        'control': {
            'format': 'Control byte: {{data.control}}'
        },
        'command': {
            'format': 'Command: {{data.command}}'
        },
        'parameter': {
            'format': 'Parameter: {{data.parameter}}'
        },
        'data': {
            'format': 'Data: {{data.data}}'
        }
    }

    def __init__(self):
        self.state = 'IDLE'
        self.address = 0
        self.command = 0
        self.params_left = 0

    def decode(self, frame: AnalyzerFrame):
        if frame.type == 'address':
            self.address = frame.data['address'][0]
            rw = 'Write' if frame.data['read'] == False else 'Read'
            return AnalyzerFrame('address', frame.start_time, frame.end_time, {
                'address': hex(self.address),
                'rw': rw
            })

        elif frame.type == 'data':
            data = frame.data['data'][0]

            if self.state == 'IDLE':
                if self.address == 0x3c:
                    if data == 0x00:  # Control byte
                        self.state = 'COMMAND'
                        return AnalyzerFrame('control', frame.start_time, frame.end_time, {
                            'control': hex(data)
                        })
                    else:  # Command directly
                        self.command = data
                        if self.command in INSTRUCTIONS:
                            instr = INSTRUCTIONS[self.command]
                            self.params_left = instr['params']
                            self.state = 'PARAMETERS' if self.params_left > 0 else 'IDLE'
                            return AnalyzerFrame('command', frame.start_time, frame.end_time, {
                                'command': f"{hex(self.command)} - {instr['name']} - {instr['description']}"
                            })
                        else:
                            self.state = 'IDLE'
                else:  # Data for other device
                    return AnalyzerFrame('data', frame.start_time, frame.end_time, {
                        'data': hex(data)
                    })

            elif self.state == 'COMMAND':
                self.command = data
                if self.command in INSTRUCTIONS:
                    instr = INSTRUCTIONS[self.command]
                    self.params_left = instr['params']
                    self.state = 'PARAMETERS' if self.params_left > 0 else 'IDLE'
                    return AnalyzerFrame('command', frame.start_time, frame.end_time, {
                        'command': f"{hex(self.command)} - {instr['name']} - {instr['description']}"
                    })
                else:
                    self.state = 'IDLE'

            elif self.state == 'PARAMETERS':
                self.params_left -= 1
                if self.params_left == 0:
                    self.state = 'IDLE'
                return AnalyzerFrame('parameter', frame.start_time, frame.end_time, {
                    'parameter': hex(data)
                })

        elif frame.type == 'start':
            self.state = 'IDLE'