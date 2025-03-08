## Description: Utility library for Apex: CSL ("Camino Sin Límites")
## Handles uploading, compressing, and decompressing images & PDFs.
## Developed for Python Flask + MySQL.
## Created by: @danytml

import io
import zlib
from PIL import Image

## ------------------------------
## Image Compression
## ------------------------------

def compressImage(image, max_size=(1000, 1000), quality=90):
    """
    Compress an image (JPEG) and return binary content ready for DB storage.

    Args:
        image: file path or file-like object (BytesIO or Flask file object)
        max_size: target size (width, height)
        quality: JPEG quality

    Returns:
        Compressed image as bytes (ready to store in DB)
    """
    img = Image.open(image)
    img = img.convert('RGB')
    img.thumbnail(max_size)
    
    compressed_img = io.BytesIO()
    img.save(compressed_img, format='JPEG', quality=quality)

    return compressed_img.getvalue()


## ------------------------------
## PDF Compression
## ------------------------------

def compressPdf(pdf):
    """
    Compress a PDF file and return binary content ready for DB storage.

    Args:
        pdf: file path or file-like object (BytesIO or Flask file object)

    Returns:
        Compressed PDF as bytes (ready to store in DB)
    """
    if hasattr(pdf, 'read'): 
        pdf_binary = pdf.read()
    else:  
        with open(pdf, 'rb') as file:
            pdf_binary = file.read()

    return zlib.compress(pdf_binary, level=9)


def decompressPdf(compressed_pdf):
    """
    Decompress a PDF from DB storage into its original binary form.

    Args:
        compressed_pdf: compressed PDF as bytes (from DB)

    Returns:
        Original (uncompressed) PDF as bytes
    """
    return zlib.decompress(compressed_pdf)


## ------------------------------
## Example Usage
## ------------------------------
"""
if __name__ == "__main__":
    # Example for images
    with open("example.jpg", "rb") as img_file:
        compressed_image = compressImage(img_file)

    # Example for PDFs
    compressed_pdf = compressPdf("example.pdf")
    with open("compressed_example.pdf.zlib", "wb") as f:
        f.write(compressed_pdf)

    decompressed_pdf = decompressPdf(compressed_pdf)
    with open("reconstructed_example.pdf", "wb") as f:
        f.write(decompressed_pdf)

    print("Compression & decompression test completed.")
"""