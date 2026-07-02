"""API backend for the Mutual NDA creator prototype (PL-3).

The frontend is a Next.js app in frontend/ that calls this API.
"""

import markdown
from flask import Flask, jsonify, request

from nda import build_document

app = Flask(__name__)

FIELD_NAMES = [
    "purpose", "effective_date", "term_type", "term_years", "conf_type",
    "conf_years", "governing_law", "jurisdiction",
    "party1_name", "party1_title", "party1_company", "party1_address",
    "party2_name", "party2_title", "party2_company", "party2_address",
]


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.post("/api/generate")
def generate():
    data = request.get_json(silent=True) or {}
    fields = {name: str(data.get(name, "")).strip() for name in FIELD_NAMES}
    document_md = build_document(fields)
    return jsonify({
        "markdown": document_md,
        "html": markdown.markdown(document_md, extensions=["tables"]),
    })


if __name__ == "__main__":
    app.run(debug=True)
