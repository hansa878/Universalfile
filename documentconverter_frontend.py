
# documentconverter_frontend.py
import streamlit as st
from documentconverter_backend import (
    convert_images_to_pdf,
    convert_pdf_to_images,
    ocr_image_to_word,
    grayscale_image,
    pdf_to_word,
    pdf_to_text,
    word_to_text
)
import tempfile
import os

st.set_page_config(page_title="Universal File Converter", page_icon="📄", layout="centered")
st.title("📄 Universal File Converter")
st.write("Upload a file and choose the operation you want to perform.")

# Select operation
operation = st.selectbox(
    "Select Operation",
    [
        "Convert Images to PDF",
        "Convert PDF to Images",
        "OCR: Image to Word",
        "Image to Grayscale",
        "Convert PDF to Word",
        "Convert PDF to Text",
        "Convert Word to Text"
    ]
)

uploaded_files = None
if operation in ["Convert Images to PDF"]:
    uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
else:
    uploaded_files = st.file_uploader("Upload File", type=["pdf", "docx", "jpg", "jpeg", "png"])

# Optional resize for images
resize_option = None
if operation in ["Convert Images to PDF", "Image to Grayscale"]:
    if st.checkbox("Resize Images?"):
        width = st.number_input("Width", min_value=50, value=800)
        height = st.number_input("Height", min_value=50, value=1000)
        resize_option = (width, height)

if st.button("Run Operation"):
    if not uploaded_files:
        st.warning("Please upload file(s) first.")
    else:
        if operation == "Convert Images to PDF":
            temp_paths = []
            for file in uploaded_files:
                temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                temp_path.write(file.read())
                temp_paths.append(temp_path.name)
            output = convert_images_to_pdf(temp_paths, resize_option)
            with open(output, "rb") as f:
                st.download_button("Download PDF", f, file_name="converted.pdf")

        elif operation == "Convert PDF to Images":
            file = uploaded_files
            temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_path.write(file.read())
            output_images = convert_pdf_to_images(temp_path.name)
            for img_path in output_images:
                st.image(img_path)
                with open(img_path, "rb") as f:
                    st.download_button(f"Download {os.path.basename(img_path)}", f, file_name=os.path.basename(img_path))

        elif operation == "OCR: Image to Word":
            file = uploaded_files
            temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_path.write(file.read())
            output = ocr_image_to_word(temp_path.name)
            with open(output, "rb") as f:
                st.download_button("Download Word File", f, file_name="ocr_result.docx")

        elif operation == "Image to Grayscale":
            file = uploaded_files
            output = grayscale_image(file, resize_option)
            st.image(output)
            with open(output, "rb") as f:
                st.download_button("Download Grayscale Image", f, file_name="grayscale.jpg")

        elif operation == "Convert PDF to Word":
            file = uploaded_files
            temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_path.write(file.read())
            output = pdf_to_word(temp_path.name)
            with open(output, "rb") as f:
                st.download_button("Download Word File", f, file_name="converted_from_pdf.docx")

        elif operation == "Convert PDF to Text":
            file = uploaded_files
            temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_path.write(file.read())
            output = pdf_to_text(temp_path.name)
            with open(output, "rb") as f:
                st.download_button("Download Text File", f, file_name="output_pdf_text.txt")

        elif operation == "Convert Word to Text":
            file = uploaded_files
            temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
            temp_path.write(file.read())
            output = word_to_text(temp_path.name)
            with open(output, "rb") as f:
                st.download_button("Download Text File", f, file_name="output_word_text.txt")
