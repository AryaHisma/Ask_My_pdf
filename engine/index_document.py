import os
import json
import fitz  # PyMuPDF

def index_document(file_path, filename, index_path="index/index_document.json"):
    # Baca teks dari file PDF
    try:
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Gagal membaca PDF {filename}: {e}")
        return

    if not full_text.strip():
        print(f"Tidak ada teks ditemukan dalam {filename}")
        return

    # Muat index lama jika ada
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = []
        
    # ❗ Hapus entri lama dengan nama file yang sama
    index = [entry for entry in index if entry["filename"] != filename]

    # Tambahkan ke index
    index.append({
        "filename": filename,
        "content": full_text
    })

    # Simpan kembali
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def remove_document_from_index(filename, index_path="index/index_document.json"):
    if not os.path.exists(index_path):
        return

    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)

    # Filter index tanpa file yang dihapus
    index = [entry for entry in index if entry["filename"] != filename]

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
