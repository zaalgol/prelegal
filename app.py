"""Prototype web app for creating a Mutual NDA document (PL-3)."""

from datetime import date

import markdown
from flask import Flask, render_template, request, Response

from nda import build_document

app = Flask(__name__, template_folder="web")

FIELD_NAMES = [
    "purpose", "effective_date", "term_type", "term_years", "conf_type",
    "conf_years", "governing_law", "jurisdiction",
    "party1_name", "party1_title", "party1_company", "party1_address",
    "party2_name", "party2_title", "party2_company", "party2_address",
]


def _fields_from_form() -> dict:
    return {name: request.form.get(name, "").strip() for name in FIELD_NAMES}


@app.get("/")
def index():
    return render_template("index.html", today=date.today().isoformat())


@app.post("/generate")
def generate():
    fields = _fields_from_form()
    document_md = build_document(fields)
    document_html = markdown.markdown(document_md, extensions=["tables"])
    return render_template("preview.html", document_html=document_html, fields=fields)


@app.post("/download")
def download():
    document_md = build_document(_fields_from_form())
    return Response(
        document_md,
        mimetype="text/markdown",
        headers={"Content-Disposition": "attachment; filename=Mutual-NDA.md"},
    )


if __name__ == "__main__":
    app.run(debug=True)
