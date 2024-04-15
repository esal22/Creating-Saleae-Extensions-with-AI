# HLA Generation using AI

This is an experimental project using Anthropic's claude.ai engine (Claude 3 Opus) go generate a python based HLA (High Level Analyzer) for Saleae's Logic2 software. Logic2 is the software user interface for their Logic 8, Logic Pro 8, and Logic Pro 16 series of Logic Analyzer hardware.  In this example the digital I2C signals are capture between an Adafruit Featherwing M0 and SH1107 based monochrome OLED display driver.


The following items are included in the repository:
- Source HLA (Before Code Generation)  <-- The Reference Design
- Final HLA (Expected Result After Code Generation)  <-- An example of 'success'
- Logic2 Data Capture << Source Data File (.sal)

Items to be downloaded:
- [SH1107 Datasheet](https://www.displayfuture.com/Display/datasheet/controller/SH1107.pdf)
- [Saleae High Level Analyzer (HLA) Documentation](https://support.saleae.com/extensions/high-level-analyzer-extensions)
- [Saleae High Level Analyzer Frame Types Documenation](https://support.saleae.com/extensions/analyzer-frame-types)


