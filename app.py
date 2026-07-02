"""API backend for the Mutual NDA creator prototype (PL-3).

The frontend is a Next.js app in frontend/ that calls this API.
"""

import re
from io import BytesIO

import markdown
from flask import Flask, Response, jsonify, request
from xhtml2pdf import pisa

from nda import build_document

app = Flask(__name__)

PDF_PAGE = """\
<html>
<head>
<style>
    @page {{ size: a4; margin: 2cm; }}
    body {{ font-family: Helvetica; font-size: 10pt; line-height: 1.5; }}
    h1 {{ font-size: 16pt; }}
    table {{ width: 100%; border-collapse: collapse; margin: 12pt 0; }}
    th, td {{ border: 1pt solid #999; padding: 4pt 6pt; text-align: left; }}
</style>
</head>
<body>{body}</body>
</html>
"""

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


def _fields_from_request() -> dict:
    data = request.get_json(silent=True) or {}
    return {name: str(data.get(name, "")).strip() for name in FIELD_NAMES}


@app.post("/api/generate")
def generate():
    document_md = build_document(_fields_from_request())
    return jsonify({
        "markdown": document_md,
        "html": markdown.markdown(document_md, extensions=["tables"]),
    })


def _pdf_html(document_md: str) -> str:
    # xhtml2pdf drops <ol> numbering for items with block content, so render
    # the section numbers as literal text instead of a markdown list.
    document_md = re.sub(r"^(\d+)\. ", r"\1\\. ", document_md, flags=re.MULTILINE)
    html = markdown.markdown(document_md, extensions=["tables"])
    # xhtml2pdf collapses columns whose cells are empty (e.g. the signature
    # row), so pad empty cells with a non-breaking space.
    html = re.sub(r"(<t[dh][^>]*>)(</t[dh]>)", r"\1&nbsp;\2", html)
    return PDF_PAGE.format(body=html)


@app.post("/api/download")
def download():
    document_md = build_document(_fields_from_request())
    buffer = BytesIO()
    status = pisa.CreatePDF(_pdf_html(document_md), dest=buffer)
    if status.err:
        return jsonify({"error": "PDF generation failed"}), 500
    return Response(
        buffer.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Mutual-NDA.pdf"},
    )


if __name__ == "__main__":
    app.run(debug=True)
