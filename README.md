SUBMISSION OVERVIEW:
Team Name: Tragic Bytes
Team Members: Jahnvi Arora, Rachit Khatri, Tanay Shah

The code developed creates a simple piepeline for an intelligent document system to fulfill requirements mentioned in part 1A and 1B of the problem statement. 

Workflow of 1A:

Goal: For any PDF, academic paper, report, textbook, a strcutured outline should be extracted, all headings, subheadins till H1,H2,H3, the page numbers, and document title. 

Solution: We have used PyMuPDF to parse each pdf and analyze each text block. Headings are detected using font properties, lines that are bold and large(for H1), slightly smaller or bold(for H2), or noticeably large non-bold(for H3). 

Approach: We have used heuristics to achieve this, a simple rule based approach. 
Reason for Approach: There is no resource constraint, it can be offline, <1GB, no training data needed, and easy to adapt to multi-lingual, non standard documents.
Advantage: Fast, transparent, offline, language-agnostic;
Limitation: Relies on Proper PDF formatting.

BONUS: Dealing with Multi-lingual papers:
1. The code fully relies on text extraction and is not language dependent;
2. functions like .islower() have been avoided to remove any case dependencies which would cause hindrance in languages that do not have cases, like Hindi, Chinese.
3. Heuristic property: classification simply depends on font size and boldness, not by langbuage clues.

Outcome: Multiple Tests have been done in the program to check the working of the program. 
INPUT folder has files that can be uploaded(pdfs)
OUTPUT folder stores .json files after the input files have been processed. 

File named file50 is a 50 page pdf that takes less than 2 seconds to process.

File named file6french is a pdf in french language with near accurate output file. 


Workflow of 1B: 

Goal: Given. a batch of realted PDFs, and a persona definition of a very specific job to be done, system should identify and prioritise most relevant sections from all of the documents, extracting important information, contextual needs, etc. 

Solution: We used a similar approach as 1A, PyMuPDF- based outline extraction. Then for persona-driven relevance, we ranked all extracted headings using TF-IDF vectorization and cosine similarity: each heading is compared to the combination of persona and job description. The highest ranked sections are selected. 

Approach:
A hybrid approach involving:
1. Heuristics- For header detections: Uses rules over font size and boldness as in 1A, robust, fast, language-independent.
2. Lightweight NLP(no ML model): Section ranking is done using TF-IDF vectorization(from scikit-learn), computing cosine similarity between persona+job text and every section, heading offline.
3. Sectional Content Extraction: Subsection text is heuristically extracted from PDF immediately after the chosen heading, for each top-ranked section.
Reseach for Approach:
a. Resource & Speed
b. Generelizability
c. Multilingual by design

Advantage:
Persona-driven relevance: Focus on user goals
Entirely offline, language agnostic(full Unicode handling)
Very fast

Limitation: 
Like 1A, performance and accuracy for sub-sections depends on the structure of the pdf, the better the structure of the pdf, higher the accuracy. 

Outcome:
INPUT: input_extract folder contains the PDFs for a given persona: in this case: persona.json contains the following data:
{
  "persona": "PhD Researcher in Computational Biology",
  "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
}

OUTPUT: output_extract folder contains the output PDF with metadata: document name, persona, job, timestamp;
extracted sections: per-document, page, heading, and ranked importance;
sub-sectional analysis: relevant passages directly extracted under each chosen heading. 

Demonstrated on: 
1. 4-document computational biology batch(GNNs for drug discovery) for a PHD persona
2. Tested on 3 large annual reports for finance analyst persona
3. Every batch is processed in under 10 seconds, with accurate, persona-focussed outputs. 

To conclude: 
To conclude, our solution presents a robust, efficient, and fully offline pipeline for intelligent document analysis as required by both parts of the hackathon. 

STEPS TO RUN DOCKER:
1. Run this command on terminal window: docker build --platform linux/amd64 -t adobehack:latest .
2. After putting input files in the folder for 1A(ensure output folder exists): docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none adobehack:latest python extract_outline.py
3.  You will find .json outline files for each PDF inside the output folder.
4. After putting input files in the folder for 1B(ensure output_extract folder exists): docker run --rm \
  -v $(pwd)/input_extract:/app/input_extract \
  -v $(pwd)/output_extract:/app/output_extract \
  -v $(pwd)/persona_job.json:/app/persona_job.json \
  --network none adobehack:latest
5. The output_extract/round1b_output.json file with all extracted, ranked, and summarized results.