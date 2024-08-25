# PDF IMAGE EXTRACTOR (JPEG AND PNG)

This script extracts and saves JPEG and PNG images embedded within PDF files.

The script reads PDF files in binary format, searches for embedded JPEG and PNG images
by identifying their unique byte signatures, and saves each detected image into a separate
file in a designated output directory. The output directory is named after the input PDF file
and is located in the 'results' folder. 


## Usage:
    python3 bin/main.py input_file.pdf
    python3 bin/main.py path/to/input/files

## Arguments:
    input_file.pdf (or) path/to/input/files : Path to the PDF files or a single pdf file from which images will be extracted.
