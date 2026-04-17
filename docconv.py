import base64
from mistralai.client import Mistral

with open("islamic.pdf", "rb") as f:
    pdf_bytes = f.read()

b64 = base64.b64encode(pdf_bytes).decode()

with Mistral(api_key="97ZQlsV45YrDusgZRwjArWGbh3nerFPb") as client:
    resp = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{b64}"
        },
        include_image_base64=True,
    )

    with open("output.md", "w", encoding="utf-8") as out:
        for page in resp.pages:
            out.write(page.markdown)
            out.write("\n\n")
    
    print("Output saved to output.md")
