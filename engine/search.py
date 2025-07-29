import json

def load_index(index_path="index/index.json"):
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)

def search_documents(keyword, index_path="index/index.json"):
    results = []
    index = load_index(index_path)
    for entry in index:
        if keyword.lower() in entry["text"].lower():
            pos = entry["text"].lower().find(keyword.lower())
            snippet = entry["text"][pos:pos+250].replace("\n", " ")
            results.append({
                "filename": entry["filename"],
                "snippet": snippet
            })
    return results
