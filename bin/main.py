"""
This script extracts and saves JPEG and PNG images embedded within PDF files.

The script reads PDF files in binary format, searches for embedded JPEG and PNG images
by identifying their unique byte signatures, and saves each detected image into a separate
file in a designated output directory. The output directory is named after the input PDF file
and is located in the 'results' folder. 

Usage:
    python script_name.py input_file.pdf
    python script_name.py path/to/input/files

Arguments:
    input_file.pdf / input_folder : Path to the PDF files or a single pdf file from which images will be extracted.
"""

import argparse
import os

def open_pdf(filename):
    """ 
    Opens a PDF file and reads its contents into a byte array.

    Args:
        filename (string) : pdf file path

    Returns:
        bytes_pdf (array): pdf file data in bytes array
        None: if the file extension is not 'pdf'
    """
    if not filename.endswith(".pdf"):
        return None
    
    with open(filename, "rb") as pdffile:
        bytes_pdf = bytearray(pdffile.read())

    return bytes_pdf


def find_jpeg_signatures(byte_array):
    """
    Finds the start and end indices of JPEG files in a byte array.

    Args:
        byte_array (bytearray): A byte array representing the data to search through.

    Returns:
        List[Tuple[int, int]]: A list of tuples containing start and end indices of JPEG files.
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

    Args:
        byte_array (bytearray): A byte array representing the data to search through.

    Returns:
        List[Tuple[int, int]]: A list of tuples containing start and end indices of PNG files.
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

    Args:
        byte_array (bytearray): The entire byte array containing the image data.
        image_tuple (Tuple[int, int]): A tuple containing the start and end indices of the image.
        output_path (str): The file path where the image should be saved (including file name and extension).
    """
    start_index, end_index = image_tuple

    # Extract the image bytes from the byte array using the start and end indices
    image_bytes = byte_array[start_index:end_index]

    # Save the extracted bytes as an image
    with open(output_path, 'wb') as image_file:
        image_file.write(image_bytes)

    print(f"Image saved to {output_path}")


def save_all_images(bytes_array, image_points, filename, extension):
    """
    Saves all images extracted from the byte array to a specific directory.

    Args:
        bytes_array (bytearray): The byte array containing the image data.
        image_points (List[Tuple[int, int]]): A list of tuples where each tuple contains the start and end indices of an image.
        filename (str): The base filename used to create the directory and name the saved images.
        extension (str): The type of the image file (jpg or png).
    """
    # Create the output directory 
    output_dir = os.path.join("results", filename[:-4] + "-pdf-images")
     
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save each image
    for i, (start_index, end_index) in enumerate(image_points):
        image_filename = f"{filename[:-4]}-image-{i+1}.{extension}"
        output_path = os.path.join(output_dir, image_filename)
        
        # Extract the image bytes and save as a JPEG
        image_bytes = bytes_array[start_index:end_index]
        with open(output_path, 'wb') as image_file:
            image_file.write(image_bytes)

        print(f"Image saved to {output_path}")


def process_file(filepath):
    """ 
    Processes a single PDF file to extract and save images.

    Args:
        filepath (str): Path to the PDF file.
    """
    pdf_bytes = open_pdf(filepath)
    filename = os.path.basename(filepath)
    if(pdf_bytes):
        jpg_image_points = find_jpeg_signatures(pdf_bytes)
        if jpg_image_points:
            print("Starting to save jpg images from the file...")
            save_all_images(pdf_bytes, jpg_image_points, filename, "jpg")
        else:
            print("No jpg signature found in the file: " + filepath)

        png_image_points = find_png_signatures(pdf_bytes)
        if png_image_points:
            print("Starting to save png images from the file...")
            save_all_images(pdf_bytes, png_image_points, filename, "png")
        else:
            print("No png signature found in the file. " + filepath)


def main(args):
    """ 
    Main function to handle the input file or directory and process accordingly.

    Args:
        args: Command-line arguments.
    """
    if os.path.isfile(args.infile):
        process_file(args.infile)
    elif os.path.isdir(args.infile):
        for filename in os.listdir(args.infile):
            filepath = os.path.join(args.infile, filename)
            if os.path.isfile(filepath):
                process_file(filepath)
    else:
        print("The provided path is neither a file nor a directory.")


if __name__ == '__main__':
    USAGE = 'Script to extract and save images (JPEG, PNG) from a PDF file or all PDFs in a directory.'
    parser = argparse.ArgumentParser(description=USAGE)
    parser.add_argument('infile', type=str, help='Input file or directory')
    args = parser.parse_args()
    main(args)
