"""Brief description of what the script does."""

import argparse
import os

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


def find_jpeg_signatures(byte_array):
    """
    Finds the start and end indices of JPEG files in a byte array.

    A JPEG file typically starts with the following byte sequence:
    - 0xFF (first byte)
    - 0xD8 (second byte)
    - 0xFF (third byte)
    - 0xE0 to 0xEF (fourth byte, a range representing JPEG markers)

    The end of a JPEG file is marked by the following byte sequence:
    - 0xFF (second-to-last byte)
    - 0xD9 (last byte)

    This function iterates over the provided byte array and identifies the indices
    where these sequences occur, effectively marking the boundaries of each JPEG file.

    Args:
        byte_array (bytearray): A byte array representing the data to search through.

    Returns:
        List[Tuple[int, int]]: A list of tuples, each containing two integers:
                               - The starting index of the JPEG file
                               - The ending index (inclusive) of the JPEG file
    """
    first_begin_signature_symbol = 0xff
    second_begin_signature_symbol = 0xd8
    end_signature = [0xff, 0xd9]

    signatures = []
    i = 0
    while i < len(byte_array) - 3:
        if (
            byte_array[i] == first_begin_signature_symbol and
            byte_array[i + 1] == second_begin_signature_symbol and
            byte_array[i + 2] == first_begin_signature_symbol and
            0xe0 <= byte_array[i + 3] <= 0xef
        ):
            start_index = i
            # Look for the end signature
            end_index = start_index
            while end_index < len(byte_array) - 1:
                if byte_array[end_index] == end_signature[0] and byte_array[end_index + 1] == end_signature[1]:
                    end_index += 2  # Include the end signature itself
                    break
                end_index += 1
            signatures.append((start_index, end_index))
            i = end_index  # Move index to the end of the found JPEG
        else:
            i += 1

    return signatures


def find_png_signatures(byte_array):
    """
    Finds the start and end indices of PNG files in a byte array.

    A PNG file always starts with the following byte sequence:
    - 137 (0x89 in hexadecimal)
    - 80 (0x50 in hexadecimal)
    - 78 (0x4E in hexadecimal)
    - 71 (0x47 in hexadecimal)
    - 13 (0x0D in hexadecimal)
    - 10 (0x0A in hexadecimal)
    - 26 (0x1A in hexadecimal)
    - 10 (0x0A in hexadecimal)

    The end of a PNG file is marked by the following byte sequence:
    - 73 (0x49 in hexadecimal)
    - 69 (0x45 in hexadecimal)
    - 78 (0x4E in hexadecimal)
    - 68 (0x44 in hexadecimal)
    - 174 (0xAE in hexadecimal)
    - 66 (0x42 in hexadecimal)
    - 96 (0x60 in hexadecimal)
    - 130 (0x82 in hexadecimal)

    This function iterates over the provided byte array and identifies the indices
    where these sequences occur, effectively marking the boundaries of each PNG file.

    Args:
        byte_array (bytearray): A byte array representing the data to search through.

    Returns:
        List[Tuple[int, int]]: A list of tuples, each containing two integers:
                               - The starting index of the PNG file
                               - The ending index (inclusive) of the PNG file
    """
    png_signature = [137, 80, 78, 71, 13, 10, 26, 10]
    end_signature = [73, 69, 78, 68, 174, 66, 96, 130]
    signature_length = len(png_signature)

    signatures = []
    i = 0
    while i < len(byte_array) - signature_length:
        if list(byte_array[i:i + signature_length]) == png_signature:
            start_index = i
            # Look for the end signature
            end_index = start_index
            while end_index < len(byte_array) - len(end_signature):
                if list(byte_array[end_index:end_index + len(end_signature)]) == end_signature:
                    end_index += len(end_signature)  # Include the end signature itself
                    break
                end_index += 1
            signatures.append((start_index, end_index))
            i = end_index  # Move index to the end of the found PNG
        else:
            i += 1

    return signatures

def save_image_from_bytes(byte_array, image_tuple, output_path):
    """
    Saves a portion of a byte array as an image file.

    This function extracts the bytes corresponding to an image from the provided byte array,
    based on the given start and end indices. It then saves this extracted byte sequence
    as a JPEG image at the specified output path.

    Args:
        byte_array (bytearray): The entire byte array containing the image data.
        image_tuple (Tuple[int, int]): A tuple containing the start and end indices of the image.
        output_path (str): The file path where the image should be saved (including file name and extension).

    Returns:
        None
    """
    start_index, end_index = image_tuple

    # Extract the image bytes from the byte array using the start and end indices
    image_bytes = byte_array[start_index:end_index]

    # Save the extracted bytes as a JPEG image
    with open(output_path, 'wb') as image_file:
        image_file.write(image_bytes)

    print(f"Image saved to {output_path}")


def save_all_images(bytes_array, image_points, filename):
    """
    Saves all images extracted from the byte array to a specific directory.

    This function iterates over a list of tuples containing start and end indices for each image
    in the byte array, extracts the corresponding bytes, and saves each image as a JPEG file.

    Args:
        bytes_array (bytearray): The byte array containing the image data.
        image_points (List[Tuple[int, int]]): A list of tuples where each tuple contains the start and end indices of an image.
        filename (str): The base filename used to create the directory and name the saved images.

    Returns:
        None
    """
    # Create the output directory based on the filename
    output_dir = os.path.join("sample-results", filename[:-4] + "-pdf-images")
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save each image
    for i, (start_index, end_index) in enumerate(image_points):
        image_filename = f"{filename[:-4]}-image-{i+1}.jpg"
        output_path = os.path.join(output_dir, image_filename)
        
        # Extract the image bytes and save as a JPEG
        image_bytes = bytes_array[start_index:end_index]
        with open(output_path, 'wb') as image_file:
            image_file.write(image_bytes)

        print(f"Image saved to {output_path}")



def main(args):
    """ Main function description """
    print('Input file:', args.infile)
    pdf_bytes = open_pdf(args.infile)
    image_points = find_jpeg_signatures(pdf_bytes)
    save_all_images(pdf_bytes,image_points,args.infile)
    #find_png_signatures(pdf_bytes)
   

if __name__ == '__main__':
    USAGE = 'Brief description of what the script does.'
    parser = argparse.ArgumentParser(description=USAGE)
    parser.add_argument('infile', type=str,
                        help='Input file name')
    args = parser.parse_args()
    main(args)