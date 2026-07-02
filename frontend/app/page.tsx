"use client";

import { FormEvent, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:5000";

type NdaDocument = { markdown: string; html: string };

export default function Home() {
  const [nda, setNda] = useState<NdaDocument | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData(event.currentTarget);
      const response = await fetch(`${API_URL}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(formData.entries())),
      });
      if (!response.ok) throw new Error(`API responded with ${response.status}`);
      setNda(await response.json());
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate document");
    } finally {
      setLoading(false);
    }
  }

  function download() {
    if (!nda) return;
    const blob = new Blob([nda.markdown], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "Mutual-NDA.md";
    link.click();
    URL.revokeObjectURL(url);
  }

  if (nda) {
    return (
      <main>
        <div className="toolbar">
          <button onClick={download}>Download document</button>
          <button className="link" onClick={() => setNda(null)}>
            &larr; Start over
          </button>
        </div>
        <div className="document" dangerouslySetInnerHTML={{ __html: nda.html }} />
      </main>
    );
  }

  return (
    <main>
      <h1>Mutual NDA Creator</h1>
      <p className="note">
        Fill in the key deal terms below to generate a Mutual Non-Disclosure Agreement based on the{" "}
        <a href="https://commonpaper.com/standards/mutual-nda/1.0">Common Paper Mutual NDA (v1.0)</a> template.
      </p>

      <form onSubmit={onSubmit}>
        <fieldset>
          <legend>Agreement Terms</legend>

          <label htmlFor="purpose">Purpose — how Confidential Information may be used</label>
          <textarea
            id="purpose"
            name="purpose"
            rows={2}
            required
            defaultValue="Evaluating whether to enter into a business relationship with the other party."
          />

          <label htmlFor="effective_date">Effective Date</label>
          <input
            type="date"
            id="effective_date"
            name="effective_date"
            defaultValue={new Date().toISOString().slice(0, 10)}
            required
          />

          <label>MNDA Term — the length of this MNDA</label>
          <div className="radio-row">
            <input type="radio" id="term_fixed" name="term_type" value="fixed" defaultChecked />
            <label htmlFor="term_fixed" className="inline">
              Expires <input type="text" name="term_years" defaultValue="1" size={3} /> year(s) from Effective Date
            </label>
          </div>
          <div className="radio-row">
            <input type="radio" id="term_open" name="term_type" value="until_terminated" />
            <label htmlFor="term_open" className="inline">
              Continues until terminated in accordance with the terms of the MNDA
            </label>
          </div>

          <label>Term of Confidentiality — how long Confidential Information is protected</label>
          <div className="radio-row">
            <input type="radio" id="conf_fixed" name="conf_type" value="fixed" defaultChecked />
            <label htmlFor="conf_fixed" className="inline">
              <input type="text" name="conf_years" defaultValue="1" size={3} /> year(s) from Effective Date (trade
              secrets protected as long as applicable law provides)
            </label>
          </div>
          <div className="radio-row">
            <input type="radio" id="conf_open" name="conf_type" value="perpetuity" />
            <label htmlFor="conf_open" className="inline">In perpetuity</label>
          </div>

          <label htmlFor="governing_law">Governing Law (state)</label>
          <input type="text" id="governing_law" name="governing_law" placeholder="e.g. Delaware" required />

          <label htmlFor="jurisdiction">Jurisdiction (city or county and state)</label>
          <input type="text" id="jurisdiction" name="jurisdiction" placeholder="e.g. New Castle, DE" required />
        </fieldset>

        <div className="two-col">
          {(["party1", "party2"] as const).map((party, i) => (
            <fieldset key={party}>
              <legend>Party {i + 1}</legend>
              <label htmlFor={`${party}_name`}>Name</label>
              <input type="text" id={`${party}_name`} name={`${party}_name`} required />
              <label htmlFor={`${party}_title`}>Title</label>
              <input type="text" id={`${party}_title`} name={`${party}_title`} />
              <label htmlFor={`${party}_company`}>Company</label>
              <input type="text" id={`${party}_company`} name={`${party}_company`} required />
              <label htmlFor={`${party}_address`}>Notice Address (email or postal)</label>
              <input type="text" id={`${party}_address`} name={`${party}_address`} required />
            </fieldset>
          ))}
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Generating…" : "Generate Mutual NDA"}
        </button>
        {error && <p className="error">{error}</p>}
      </form>
    </main>
  );
}
