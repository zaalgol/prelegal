"""Build a completed Mutual NDA document from the Common Paper template.

The completed document consists of a Cover Page filled in with the
user-provided deal terms, followed by the Common Paper Mutual NDA
Standard Terms (Version 1.0) from templates/Mutual-NDA.md.
"""

import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

COVER_PAGE = """\
# Mutual Non-Disclosure Agreement

This Mutual Non-Disclosure Agreement (the "MNDA") consists of: (1) this \
Cover Page and (2) the Common Paper Mutual NDA Standard Terms Version 1.0 \
below, identical to those posted at \
[commonpaper.com/standards/mutual-nda/1.0](https://commonpaper.com/standards/mutual-nda/1.0). \
Any modifications of the Standard Terms are made on the Cover Page, which \
will control over conflicts with the Standard Terms.

### Purpose

{purpose}

### Effective Date

{effective_date}

### MNDA Term

{mnda_term}

### Term of Confidentiality

{term_of_confidentiality}

### Governing Law & Jurisdiction

Governing Law: {governing_law}

Jurisdiction: {jurisdiction}

By signing this Cover Page, each party agrees to enter into this MNDA as of \
the Effective Date.

|| PARTY 1 | PARTY 2 |
|:--- | :----: | :----: |
| Signature | | |
| Print Name | {party1_name} | {party2_name} |
| Title | {party1_title} | {party2_title} |
| Company | {party1_company} | {party2_company} |
| Notice Address | {party1_address} | {party2_address} |
| Date | {effective_date} | {effective_date} |

---

"""


def _standard_terms() -> str:
    """Return the Standard Terms with cover-page references as plain bold text."""
    text = (TEMPLATES_DIR / "Mutual-NDA.md").read_text(encoding="utf-8")
    return re.sub(r'<span class="coverpage_link">(.*?)</span>', r"**\1**", text)


def build_document(fields: dict) -> str:
    """Return the completed MNDA as a Markdown string.

    Expected keys: purpose, effective_date, term_type ("fixed" or
    "until_terminated"), term_years, conf_type ("fixed" or "perpetuity"),
    conf_years, governing_law, jurisdiction, and party{1,2}_{name,title,
    company,address}.
    """
    if fields.get("term_type") == "until_terminated":
        mnda_term = "Continues until terminated in accordance with the terms of the MNDA."
    else:
        mnda_term = f"Expires {fields.get('term_years', '1')} year(s) from Effective Date."

    if fields.get("conf_type") == "perpetuity":
        term_of_confidentiality = "In perpetuity."
    else:
        term_of_confidentiality = (
            f"{fields.get('conf_years', '1')} year(s) from Effective Date, but in "
            "the case of trade secrets until Confidential Information is no longer "
            "considered a trade secret under applicable laws."
        )

    cover_page = COVER_PAGE.format(
        purpose=fields.get("purpose", ""),
        effective_date=fields.get("effective_date", ""),
        mnda_term=mnda_term,
        term_of_confidentiality=term_of_confidentiality,
        governing_law=fields.get("governing_law", ""),
        jurisdiction=fields.get("jurisdiction", ""),
        party1_name=fields.get("party1_name", ""),
        party1_title=fields.get("party1_title", ""),
        party1_company=fields.get("party1_company", ""),
        party1_address=fields.get("party1_address", ""),
        party2_name=fields.get("party2_name", ""),
        party2_title=fields.get("party2_title", ""),
        party2_company=fields.get("party2_company", ""),
        party2_address=fields.get("party2_address", ""),
    )
    return cover_page + _standard_terms()
