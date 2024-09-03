import subprocess
import sys
import os

# Function to install a package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check if the fitz (PyMuPDF) module is installed
try:
    import fitz  # PyMuPDF
except ImportError:
    print("The fitz (PyMuPDF) module is not found. Installing...")
    install('PyMuPDF')
    import fitz  # Import after installation

# Prompt the user for the PDF file path
pdf_path = input("Enter the full path to the PDF file: ").strip()

# Check if the specified file exists
if not os.path.isfile(pdf_path):
    print(f"The file at {pdf_path} was not found.")
    sys.exit(1)

# Prompt the user for the save path for images
save_path = input("Enter the path to save the images: ").strip()

# Check if the save directory exists
if not os.path.exists(save_path):
    os.makedirs(save_path)
    print(f"Directory {save_path} created.")

# Open the PDF file
pdf_file = fitz.open(pdf_path)

# Iterate through all the pages of the PDF
for page_index in range(len(pdf_file)):
    page = pdf_file.load_page(page_index)
    images = page.get_images(full=True)
    
    for image_index, img in enumerate(images):
        xref = img[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_name = os.path.join(save_path, f"image_page_{page_index+1}_{image_index+1}.{image_ext}")

        # Save the image to disk
        with open(image_name, "wb") as image_file:
            image_file.write(image_bytes)

pdf_file.close()

print(f"Images have been successfully extracted and saved to {save_path}.")