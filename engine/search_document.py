import json

def load_index(index_path="index/index_document.json"):
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)

def search_documents(keyword, index_path="index/index_document.json"):
    results = []
    index = load_index(index_path)
    for entry in index:
        if keyword.lower() in entry["content"].lower():
            pos = entry["content"].lower().find(keyword.lower())
            snippet = entry["content"][pos:pos+250].replace("\n", " ")
            results.append({
                "filename": entry["filename"],
                "snippet": snippet
            })
    return results
