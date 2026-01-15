import fitz  
from tqdm import tqdm


def load_pdf_blocks(pdf_path: str):
    """
    Extract text blocks with font size information from PDF.
    """
    doc = fitz.open(pdf_path) #path is agnostic
    extracted = []

    for page_idx in tqdm(range(len(doc)), desc="Reading PDF"):
        page = doc[page_idx]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    extracted.append(
                        {
                            "text": text,
                            "font_size": span["size"],
                            "page_number": page_idx + 1
                        }
                    )

    return extracted


def classify_block(text: str, font_size: float):
    """
    Classify a text span based on content and font size.
    """
    text_l = text.lower()

    if text_l.startswith("chapter"):
        return "chapter"

    if font_size >= 16:
        return "topic"

    if font_size >= 13:
        return "subtopic"

    return "body"
