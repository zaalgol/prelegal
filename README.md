# prelegal

🚧 **This project is a work in progress.**

Documentation and code are still being developed — this README will be updated as the project evolves.

## Mutual NDA Creator (prototype)

A web application that creates a Mutual NDA document. Fill in the key deal
terms in a form, preview the completed agreement, and download it as a
Markdown file. Based on the [Common Paper Mutual NDA (v1.0)](https://commonpaper.com/standards/mutual-nda/1.0)
template in `templates/`.

### Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Legal document templates

The `templates/` directory contains legal agreement templates curated from
[Common Paper](https://github.com/CommonPaper) (CC BY 4.0). `catalog.json`
describes each document.
