"""Brief description of what the script does."""

import argparse

def open_pdf(filename):
    """ 
    Args:
        filename (string) : pdf file path

    Returns:
        bytes_pdf (array): pdf file data in bytes array

    Raises:
        ValueError: if filename does't end with '.pdf'          
    """
    if (filename[-4:]!=".pdf"):
        raise ValueError("File extension must be '.pdf'")
    
    bytes_pdf = []
    with open(filename,"rb") as pdffile:
        bytes_pdf = bytearray(pdffile.read())

    return bytes_pdf


def find_jpeg_start_signatures(byte_array):
    print(byte_array[0:5])
    """
    Finds the starting indices of JPEG files in a byte array based on the JPEG signature.

    A JPEG file typically starts with the following byte sequence:
    - 0xFF (first byte)
    - 0xD8 (second byte)
    - 0xFF (third byte)
    - 0xE0 to 0xEF (fourth byte, a range representing JPEG markers)

    This function iterates over the provided byte array and identifies the indices
    where this sequence occurs.

    Args:
        byte_array (bytearray): A byte array representing the data to search through.

    Returns:
        List[int]: A list of integers representing the starting indices of the found JPEG signatures.
    """
    first_begin_signature_symbol = 0xff
    second_begin_signature_symbol = 0xd8

    indexes = []
    for index in range(len(byte_array) - 3):
        if (
            byte_array[index] == first_begin_signature_symbol and
            byte_array[index + 1] == second_begin_signature_symbol and
            byte_array[index + 2] == first_begin_signature_symbol and
            0xe0 <= byte_array[index + 3] <= 0xef
        ):
            indexes.append(index)
    print(indexes)
    return indexes

def find_png_start_signatures(byte_array):
    """
    Finds the starting indices of PNG files in a byte array based on the PNG signature.

    A PNG file always starts with the following byte sequence:
    - 137 (0x89 in hexadecimal)
    - 80 (0x50 in hexadecimal)
    - 78 (0x4E in hexadecimal)
    - 71 (0x47 in hexadecimal)
    - 13 (0x0D in hexadecimal)
    - 10 (0x0A in hexadecimal)
    - 26 (0x1A in hexadecimal)
    - 10 (0x0A in hexadecimal)

    This function iterates over the provided byte array and identifies the indices
    where this sequence occurs.

    Args:
        byte_array (bytearray): A byte array representing the data to search through.

    Returns:
        List[int]: A list of integers representing the starting indices of the found PNG signatures.
    """
    png_signature = [137, 80, 78, 71, 13, 10, 26, 10]
    signature_length = len(png_signature)

    indexes = []
    for index in range(len(byte_array) - signature_length + 1):
        if list(byte_array[index:index + signature_length]) == png_signature:
            indexes.append(index)

    print("PNG start signatures found at indices:", indexes)
    return indexes



def main(args):
    """ Main function description """
    print('Input file:', args.infile)
    pdf_bytes = open_pdf(args.infile)
    find_jpeg_start_signatures(pdf_bytes)
    find_png_start_signatures(pdf_bytes)
   

if __name__ == '__main__':
    USAGE = 'Brief description of what the script does.'
    parser = argparse.ArgumentParser(description=USAGE)
    parser.add_argument('infile', type=str,
                        help='Input file name')
    args = parser.parse_args()
    main(args)