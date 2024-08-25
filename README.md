# PDF IMAGE EXTRACTOR (JPEG AND PNG)

This script extracts and saves JPEG and PNG images embedded within PDF files.

The script reads PDF files in binary format, searches for embedded JPEG and PNG images
by identifying their unique byte signatures, and saves each detected image into a separate
file in a designated output directory. The output directory is named after the input PDF file
and is located in the 'results' folder. 


## Usage:
    - python script_name.py input_file.pdf
    - python script_name.py path/to/input/files

## Arguments:
    - input_file.pdf / input_folder : Path to the PDF files or a single pdf file from which images will be extracted.