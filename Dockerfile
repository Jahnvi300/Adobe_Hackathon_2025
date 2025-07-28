FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY extract_outline.py .
COPY intelligent_extractor.py .

RUN mkdir input output
RUN mkdir input_extract output_extract

CMD ["python", "intelligent_extractor.py"]
