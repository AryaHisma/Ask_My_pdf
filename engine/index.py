import os
import json
import fitz  # PyMuPDF

def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def extract_all_texts(data_folder="data_pdf", index_path="index/index.json"):
    index = []
    for fname in os.listdir(data_folder):
        if fname.endswith(".pdf") or fname.endswith(".txt"):
            path = os.path.join(data_folder, fname)
            text = extract_text_from_pdf(path) if fname.endswith(".pdf") else extract_text_from_txt(path)
            index.append({"filename": fname, "text": text})
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    extract_all_texts()
    print("Index selesai dibuat.")
