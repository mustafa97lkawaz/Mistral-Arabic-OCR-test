import base64
import os
from mistralai.client import Mistral
from pdf2image import convert_from_path
import PyPDF2

PDF_FILE = "islamic.pdf"
OUTPUT_FOLDER = "ocr_output"
START_PAGE = 1

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

POPPLER_PATH = r"C:\poppler\poppler-24.08.0\Library\bin"

reader = PyPDF2.PdfReader(PDF_FILE)
total_pages = len(reader.pages)
print(f"Total PDF pages: {total_pages}")

if START_PAGE == 1:
    print("Converting PDF to images...")
    images = convert_from_path(PDF_FILE, poppler_path=POPPLER_PATH)
else:
    print(f"Converting pages {START_PAGE} to {total_pages}...")
    images = convert_from_path(PDF_FILE, poppler_path=POPPLER_PATH, first_page=START_PAGE, last_page=total_pages)

print(f"Converting done")
print(f"Number of images: {len(images)}")

with Mistral(api_key="97ZQlsV45YrDusgZRwjArWGbh3nerFPb") as client:
    for i, image in enumerate(images):
        page_num = START_PAGE + i
        image_path = os.path.join(OUTPUT_FOLDER, f"page_{page_num}.png")
        image.save(image_path, "PNG")
        
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        
        img_b64 = base64.b64encode(img_bytes).decode()
        
        resp = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "image_url",
                "image_url": f"data:image/png;base64,{img_b64}"
            },
        )
        
        text_file_path = os.path.join(OUTPUT_FOLDER, f"page_{page_num}.txt")
        with open(text_file_path, "w", encoding="utf-8") as out:
            out.write(resp.pages[0].markdown)
        
        print(f"Page {page_num} processed and saved to {text_file_path}")

print(f"All pages processed. Output saved to {OUTPUT_FOLDER}/")
