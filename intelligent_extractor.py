# import os
# import json
# import time
# from datetime import datetime

# # For TF-IDF vectorization
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# from extract_outline import extract_outline  # Use YOUR function!

# INPUT_DIR = "input_extract"
# OUTPUT_DIR = "output_extract"
# PERSONA_JOB_FILE = "persona_job.json"

# def read_persona_job(fname):
#     with open(fname, "r", encoding="utf-8") as f:
#         pj = json.load(f)
#     return pj["persona"], pj["job_to_be_done"]

# def collect_all_outlines(input_dir):
#     outlines = []
#     doc_names = []
#     for fname in sorted(os.listdir(input_dir)):
#         if not fname.lower().endswith(".pdf"):
#             continue
#         doc_path = os.path.join(input_dir, fname)
#         outline = extract_outline(doc_path)
#         outlines.append({"document": fname, "outline": outline["outline"]})
#         doc_names.append(fname)
#     return outlines, doc_names

# def expand_sections(flat_outlines):
#     """Turn outline list into separate section dicts with doc/page/title/level"""
#     sections = []
#     for doc in flat_outlines:
#         pdfname = doc["document"]
#         for section in doc["outline"]:
#             sections.append({
#                 "document": pdfname,
#                 "section_title": section["text"],
#                 "level": section["level"],
#                 "page_number": section["page"]
#             })
#     return sections

# def compute_scores(sections, ref_text):
#     """Compute similarity of each section to the persona/job string"""
#     texts = [ref_text] + [s["section_title"] for s in sections]
#     vectorizer = TfidfVectorizer().fit(texts)
#     vectors = vectorizer.transform(texts)
#     sims = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
#     for i, s in enumerate(sections):
#         s["relevance_score"] = float(sims[i])
#     return sections

# def rank_sections(sections, top_n=10):
#     ranked = sorted(sections, key=lambda x: -x["relevance_score"])
#     for i, s in enumerate(ranked[:top_n]):
#         s["importance_rank"] = i + 1
#     return ranked[:top_n]

# def extract_subsection_text(pdf_path, page_num, heading_text, max_blocks=3):
#     """
#     Extract the text(s) after the heading on the same page.
#     """
#     import fitz  # PyMuPDF
#     blocks = []
#     try:
#         doc = fitz.open(pdf_path)
#         page = doc[page_num - 1]
#         all_blocks = page.get_text("blocks")  # [[x0,y0,x1,y1,"text", ...], ...]
#         start_found = False
#         for b in all_blocks:
#             text = b[4].strip()
#             if not text:
#                 continue
#             # Look for heading; then start collecting subsequent blocks
#             if not start_found and heading_text.strip().lower() in text.lower():
#                 start_found = True
#                 continue  # skip the heading line
#             if start_found and text:
#                 blocks.append(text)
#                 if len(blocks) >= max_blocks:
#                     break
#         if not blocks:
#             # If nothing found, just take the first non-heading block
#             blocks = [b[4].strip() for b in all_blocks if b[4].strip()][1:max_blocks+1]
#         return " ".join(blocks).strip()
#     except Exception as e:
#         return ""
    
# def main():
#     t0 = time.time()
#     # Ensure output directory exists
#     os.makedirs(OUTPUT_DIR, exist_ok=True)

#     # Step 1: Load persona and job
#     persona, job = read_persona_job(PERSONA_JOB_FILE)
#     persona_job_text = persona + " " + job

#     # Step 2: Extract outlines from all PDFs in input/
#     outlines, doc_names = collect_all_outlines(INPUT_DIR)
#     all_sections = expand_sections(outlines)

#     # Step 3: Score and rank sections for relevance
#     scored_sections = compute_scores(all_sections, persona_job_text)
#     top_sections = rank_sections(scored_sections, top_n=10)

#     # Step 4: For each selected section, extract a "relevant" sub-section
#     sub_sections = []
#     for s in top_sections:
#         pdf_path = os.path.join(INPUT_DIR, s["document"])
#         refined_text = extract_subsection_text(pdf_path, s["page_number"], s["section_title"])
#         sub_sections.append({
#             "document": s["document"],
#             "parent_section_title": s["section_title"],
#             "refined_text": refined_text,
#             "page_number": s["page_number"]
#         })

#     # Step 5: Assemble output as required by challenge
#     output = {
#         "metadata": {
#             "input_documents": doc_names,
#             "persona": persona,
#             "job_to_be_done": job,
#             "processing_timestamp": datetime.now().isoformat(timespec='seconds')
#         },
#         "extracted_sections": [
#             {
#                 "document": s["document"],
#                 "page_number": s["page_number"],
#                 "section_title": s["section_title"],
#                 "importance_rank": s["importance_rank"]
#             }
#             for s in top_sections
#         ],
#         "subsection_analysis": sub_sections
#     }

#     # Step 6: Write output
#     outpath = os.path.join(OUTPUT_DIR, "round1b_output.json")
#     with open(outpath, "w", encoding="utf-8") as f:
#         json.dump(output, f, indent=2, ensure_ascii=False)

#     print(f"Done in {time.time() - t0:.2f}s. Output written to: {outpath}")

# if __name__ == "__main__":
#     main()

# Jahnvi Arora/Rachit Khatri/Tanay Shah
# Team Name: Tragic Bytes
# Adobe Hackathon 2025 - Persona-Driven PDF Section Extractor (Round 1B)

import os
import json
import time
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from extract_outline import extract_outline

IN_DIR = "input_extract"
OUT_DIR = "output_extract"
PERSONA_FILE = "persona_job1.json"

def read_persona(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            rec = json.load(f)
            return rec.get("persona", ""), rec.get("job_to_be_done", "")
    except Exception as e:
        print(f"[ERROR] Failed to read persona_job1.json: {e}")
        return "", ""

def gather_outlines(folder):
    outlist, filenames = [], []
    all_files = sorted(os.listdir(folder))
    for fname in all_files:
        if not fname.lower().endswith(".pdf"):
            continue
        doc_path = os.path.join(folder, fname)
        outline_result = extract_outline(doc_path)
        outlist.append({"document": fname, "outline": outline_result["outline"]})
        filenames.append(fname)
    return outlist, filenames

def flatten_sections(outlines):
    flat = []
    for doc in outlines:
        for sect in doc.get("outline", []):
            flat.append({
                "document": doc["document"],
                "section_title": sect["text"],
                "level": sect["level"],
                "page_number": sect["page"]
            })
    return flat

def score_sections(sections, persona_str, job_str):
    # Vectorize all headings against persona/job as ref
    context = f"{persona_str} {job_str}"
    corpus = [context] + [s["section_title"] for s in sections]
    tfidf = TfidfVectorizer().fit(corpus)
    v = tfidf.transform(corpus)
    sims = cosine_similarity(v[0:1], v[1:]).flatten()
    for i, s in enumerate(sections):
        s["relevance_score"] = float(sims[i])
    return sections

def pick_sections(scored, n=10):
    ranked = sorted(scored, key=lambda s: -s.get("relevance_score", 0))
    for rank, sec in enumerate(ranked[:n]):
        sec["importance_rank"] = rank + 1
    return ranked[:n]

def extract_snippet(pdf_path, pg_no, heading, max_blocks=3):
    import fitz
    lines = []
    try:
        doc = fitz.open(pdf_path)
        pg = doc[pg_no - 1]
        blks = pg.get_text("blocks")
        grab = False
        for block in blks:
            txt = block[4].strip()
            if not txt:
                continue
            if not grab and heading.strip() in txt:
                grab = True
                continue
            if grab:
                lines.append(txt)
                if len(lines) >= max_blocks:
                    break
        if not lines and blks:
            lines = [blk[4].strip() for blk in blks if blk[4].strip()][1:max_blocks+1]
        return " ".join(lines).strip()
    except Exception as e:
        print(f"[WARN] Could not extract snippet on p{pg_no} of {os.path.basename(pdf_path)}: {e}")
        return ""

def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)

    persona, job = read_persona(PERSONA_FILE)
    outlines, doc_list = gather_outlines(IN_DIR)
    all_sections = flatten_sections(outlines)
    scored = score_sections(all_sections, persona, job)
    picks = pick_sections(scored, n=10)

    sub_sections = []
    for sec in picks:
        doc_path = os.path.join(IN_DIR, sec["document"])
        snippet = extract_snippet(doc_path, sec["page_number"], sec["section_title"])
        sub_sections.append({
            "document": sec["document"],
            "parent_section_title": sec["section_title"],
            "refined_text": snippet,
            "page_number": sec["page_number"]
        })

    result = {
        "metadata": {
            "input_documents": doc_list,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat(timespec='seconds')
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "page_number": sec["page_number"],
                "section_title": sec["section_title"],
                "importance_rank": sec["importance_rank"]
            }
            for sec in picks
        ],
        "subsection_analysis": sub_sections
    }
    outpath = os.path.join(OUT_DIR, "round1b_output.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Round 1B finished in {time.time() - t0:.2f} sec. Output: {outpath}")

if __name__ == "__main__":
    main()

