# Creating-Saleae-Extensions-with-AI

The overall goal is to use Generative AI to create extensions for Saleae Logic 2.  I'm starting with a Python based HLA (High Level Analyzer) and will expand from there.

## Diagram of the Current Objective

![HLA Diagram](https://github.com/esal22/Creating-Saleae-Extensions-with-AI/blob/491fd252b1eb2f2549f8b062f2ac50e7064cc370/High%20Level%20Analyzer/SH1107%20Decoder%20Project/Claude%20for%20Generating%20HLA.png)

## Software Needed to Get Started?
- [Download Logic 2](https://www.saleae.com/pages/downloads)

---

## Experiment 0: Can Generative AI decode a datahsheet?
### Objective
 Providing the datasheet as context, can the generative AI interpret instructions
### Steps
- Upload datasheet for the SH1107
- Copy/Paste I2C Received Frames from the Logic 2 Terminal
- Can Claude understand the instructions?
### Resources
- Required Software: [Download Logic 2](https://www.saleae.com/pages/downloads)
- Source Data File: [SH1107-data-file.sal](/High%20Level%20Analyzer/SH1107%20Decoder%20Project/Logic2%20Data%20Capture)
### Status
- Status:  *Success*
- Link: [YouTube Video](https://youtu.be/x-kMQCyVMyI?feature=shared)

  
---

## Experiment 1: Create a device specific HLA that can Decode I2C frames
### Objective
  Can generative AI be used to generate a HLA that recognizes and decodes I2C frames, placing human readable annotations above each received frame. Note: The SH1107 OLED Driver part is chosen because I had it on hand, and it has an interesting state machine supporting both commands and data with multi-byte instructions.
### Steps
- Provide Generative AI context (Datasheet, API reference, example code)
- Ask the generative AI to provide an outline.
- Ask the generate to modify the HLA python file.
- Load it into Logic 2 and see if it can successfully decode the reference .sal data file.
### Resources
- Required Software: [Download Logic 2](https://www.saleae.com/pages/downloads)
- Source Data File: [SH1107-data-file.sal]
- [SH1107 Decoder HLA Source Files](/High%20Level%20Analyzer/SH1107%20Decoder%20Project)
### Status
- Status: *success*
- Created a basic HLA Decoder from the SH1107 (Monochrome OLED Driver)
  - Note: The lookup table is incomplete and more commands need to be added, but it seems to work properly on first pass
- Link: (coming soon)

