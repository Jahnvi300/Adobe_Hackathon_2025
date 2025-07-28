# import os
# import json
# import fitz  # PyMuPDF
# import time

# # Use project-relative paths
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# INPUT_DIR = os.path.join(BASE_DIR, "input")
# OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# def extract_outline(pdf_path):
#     doc = fitz.open(pdf_path)
#     outline = []
#     title = os.path.splitext(os.path.basename(pdf_path))[0]

#     meta_title = doc.metadata.get('title') or None
#     if meta_title:
#         title = meta_title

#     heading_candidates = []
#     for i, page in enumerate(doc):
#         blocks = page.get_text("dict")["blocks"]
#         for block in blocks:
#             if block['type'] == 0:
#                 for line in block['lines']:
#                     text = "".join([span['text'] for span in line['spans']]).strip()
#                     if len(text) < 3 or text.islower():
#                         continue
#                     for span in line['spans']:
#                         size = span['size']
#                         font = span['font']
#                         is_bold = "Bold" in font
#                         if is_bold and size > 12:
#                             level = "H1"
#                         elif is_bold and 10 < size <= 12:
#                             level = "H2"
#                         elif size > 11 and not is_bold:
#                             level = "H3"
#                         else:
#                             continue
#                         heading_candidates.append({
#                             "level": level,
#                             "text": text,
#                             "page": i + 1
#                         })
#                         break

#     seen = set()
#     for h in heading_candidates:
#         key = (h['text'], h['page'], h['level'])
#         if key not in seen:
#             outline.append(h)
#             seen.add(key)

#     return {"title": title, "outline": outline}

# def main():
#     os.makedirs(INPUT_DIR, exist_ok=True)
#     os.makedirs(OUTPUT_DIR, exist_ok=True)

#     input_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.pdf')]
#     for filename in input_files:
#         pdf_path = os.path.join(INPUT_DIR, filename)
#         json_path = os.path.join(OUTPUT_DIR, filename.replace('.pdf', '.json'))
#         start_time = time.time() 
#         result = extract_outline(pdf_path)
#         elapsed = (time.time() - start_time) * 1000 
#         with open(json_path, "w", encoding="utf-8") as fout:
#             json.dump(result, fout, indent=2, ensure_ascii=False)
#         print(f"{filename}: Processing took {elapsed:.2f} ms")  # Print the timing

# if __name__ == "__main__":
#     main()


# import os
# import fitz          # PyMuPDF for PDF processing
# import json
# import time

# # Set up paths based on the script location
# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# PDF_INPUT_DIR = os.path.join(PROJECT_ROOT, "input")
# PDF_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# def extract_outline(pdf_path):
#     doc = fitz.open(pdf_path)
#     headings_found = []
#     base_title = os.path.splitext(os.path.basename(pdf_path))[0]
#     outline_title = doc.metadata.get('title') or base_title

#     # Loop through each page and extract blocks of text
#     for page_idx, page in enumerate(doc):
#         text_blocks = page.get_text("dict")["blocks"]
#         for block in text_blocks:
#             if block.get('type') == 0:   # type 0 is text
#                 for line in block["lines"]:
#                     content = "".join(span["text"] for span in line["spans"]).strip()
#                     # Only keep text lines sufficiently long (no font-case filter for multilingual!)
#                     if len(content) < 3:
#                         continue
#                     for span in line["spans"]:
#                         font_size = span["size"]
#                         font_desc = span["font"]
#                         is_bold = "Bold" in font_desc
#                         # Heuristic for heading levels (works across scripts/languages)
#                         if is_bold and font_size > 12:
#                             heading_level = "H1"
#                         elif is_bold and 10 < font_size <= 12:
#                             heading_level = "H2"
#                         elif font_size > 11 and not is_bold:
#                             heading_level = "H3"
#                         else:
#                             continue
#                         headings_found.append({
#                             "level": heading_level,
#                             "text": content,
#                             "page": page_idx + 1
#                         })
#                         break  # Only capture one heading-type per line

#     # Remove duplicates while preserving order (text, page, level tuple as key)
#     deduped = []
#     seen_keys = set()
#     for h in headings_found:
#         key = (h["text"], h["page"], h["level"])
#         if key not in seen_keys:
#             deduped.append(h)
#             seen_keys.add(key)

#     return {
#         "title": outline_title,
#         "outline": deduped
#     }

# def main():
#     # Make sure input/output folders are there
#     os.makedirs(PDF_INPUT_DIR, exist_ok=True)
#     os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)

#     pdf_files = [name for name in os.listdir(PDF_INPUT_DIR) if name.lower().endswith(".pdf")]
#     for fname in pdf_files:
#         file_path = os.path.join(PDF_INPUT_DIR, fname)
#         out_path = os.path.join(PDF_OUTPUT_DIR, fname.replace('.pdf', '.json'))
#         started = time.time()
#         outline_result = extract_outline(file_path)
#         elapsed_ms = (time.time() - started) * 1000
#         with open(out_path, "w", encoding="utf-8") as fp:
#             json.dump(outline_result, fp, indent=2, ensure_ascii=False)
#         print(f'Processed {fname} in {elapsed_ms:.1f} ms')

# if __name__ == "__main__":
#     # Our heading extractor works for any language PDF, as long as the text is selectable — great for multilingual corpora!
#     main()


#Jahnvi Arora: 1a
# Adobe Hackathon 2025 - PDF Outline Extractor
# Team Name: Tragic Bytes

import os
import fitz  
import json
import time

# Project-relative folder setup
BASE_PATH = os.path.dirname(__file__)
IN_DIR = os.path.join(BASE_PATH, "input")
OUT_DIR = os.path.join(BASE_PATH, "output")

def extract_outline(pdf_file):
    # Attempt to open PDF
    try:
        pdf_doc = fitz.open(pdf_file)
    except Exception as err:
        print(f"[WARN] Couldn't open: {pdf_file} ({err})")
        return {"title": None, "outline": []}

    # Try to grab a 'title' from metadata if present
    meta_title = pdf_doc.metadata.get('title') or None
    doc_title = meta_title if meta_title else os.path.splitext(os.path.basename(pdf_file))[0]
    heading_items = []

    # Page loop
    for pg_num, page in enumerate(pdf_doc):
        try:
            blocks = page.get_text("dict").get("blocks", [])
        except Exception as e:
            # Sometimes OCR or weird PDF error; skip page
            print(f"[INFO] Skipping page {pg_num+1}: {e}")
            continue

        for block in blocks:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                text_line = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
                if not text_line or len(text_line) < 3:
                    continue        # skip lines not required
                # Heading logic: font size, bold, etc.
                for sp in line.get("spans", []):
                    fname = sp.get("font", "")
                    sz = sp.get("size", 0)
                    level = None
                    if "Bold" in fname and sz > 12:
                        level = "H1"
                    elif "Bold" in fname and 10 < sz <= 12:
                        level = "H2"
                    elif sz > 11 and "Bold" not in fname:
                        level = "H3"
                    else:
                        continue
                    heading_items.append({
                        "level": level,
                        "text": text_line,
                        "page": pg_num+1
                    })
                    break  # Only record one level per line

    # Deduplicate while preserving order
    deduped, seen = [], set()
    for item in heading_items:
        tup = (item["text"], item["page"], item["level"])
        if tup not in seen:
            deduped.append(item)
            seen.add(tup)

    return {"title": doc_title, "outline": deduped}

def main():
    os.makedirs(IN_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    pdf_list = [f for f in os.listdir(IN_DIR) if f.lower().endswith(".pdf")]

    for file in pdf_list:
        full_path = os.path.join(IN_DIR, file)
        json_out = os.path.join(OUT_DIR, file.replace(".pdf", ".json"))
        t0 = time.time()
        outline_struct = extract_outline(full_path)
        delta = (time.time() - t0) * 1000
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(outline_struct, f, indent=2, ensure_ascii=False)
        print(f"{file} -> {os.path.basename(json_out)} ({delta:.1f}ms)")

if __name__ == "__main__":
    main()


