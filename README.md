# Creating-Saleae-Extensions-with-AI

The overall goal is to use Generative AI to create extensions for Saleae Logic2.  I'm starting with a Python based HLA (High Level Analyzer) and will expand from there.

## Project 0: Can Generative AI decode a datahsheet?
### Objective
 Providing the datasheet as context, can the generative AI interpret instructions
### Steps
- Upload datasheet for the SH1107
- Copy/Paste I2C Received Frames from the Logic2 Terminal
- Can Claude understand the instructions?
### Resources
- Link: [YouTube Video](https://youtu.be/x-kMQCyVMyI?feature=shared)
- Resulting Data file: [SH1107-data-file.sal](/High%20Level%20Analyzer/SH1107%20Decoder%20Project/Logic2%20Data%20Capture)
### Status
- Status:  *Success*



## Project 1: Create a device specific HLA that can Decode I2C frames
### Objective
  Can generative AI be used to generate a HLA that recognizes and decodes I2C frames, placing human readable annotations above each received frame.
### Steps
- Provide Generative AI context (Datahseet, API reference, example code, etc...)
- Genrate the HLA python file
- Load it into Logic2 and see if it can successfully decode the reference .sal data file.
### Resources
- SH1107 part is chosen because I had it on hand, and it has an interesting state machine and supports multi-byte instructions
- [SH1107 Decoder HLA](/High%20Level%20Analyzer/SH1107%20Decoder%20Project)
### Status
- Status: *In work*
- Create a HLA Decoder from the SH1107 (Monochrome OLED Driver)
