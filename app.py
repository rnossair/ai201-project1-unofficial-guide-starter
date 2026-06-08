"""
Milestone 5: Gradio chat interface.

Retrieves the top-k most relevant chunks, sends them to Groq as grounded
context, and requires the model to cite every claim with [1], [2], etc.
"""

import os
import re
from dotenv import load_dotenv
from groq import Groq
import gradio as gr

from retrieve import retrieve

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"
TOP_K = 6

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """\
You are a helpful assistant that answers questions about the Computer Science \
experience at Grinnell College.

Rules you must follow:
1. Base your answer ONLY on the context passages in the provided documents. \
Do not use outside knowledge.
2. Cite every factual claim by mentioning the file name or url associated with the entry, this is non-negotiable.
3. When citing, use the format [1], [2], etc. corresponding to the numbered context SOURCES. If two passage are from the same source, they share the same number. \
4. If the context does not contain enough information to answer, say so clearly \
instead of guessing.
5. Be concise and direct.\
"""


def get_source_mapping(chunks: list[dict]) -> tuple[dict, list]:
    """Helper to map unique URLs to a single citation number."""
    url_to_id = {}
    unique_sources = []
    source_counter = 1
    
    for chunk in chunks:
        url = chunk["source_url"]
        if url not in url_to_id:
            url_to_id[url] = source_counter
            unique_sources.append((source_counter, chunk["source_description"], url))
            source_counter += 1
            
    return url_to_id, unique_sources


def build_user_message(query: str, chunks: list[dict]) -> str:
    url_to_id, _ = get_source_mapping(chunks)
    
    context_lines = []
    for chunk in chunks:
        cite_num = url_to_id[chunk["source_url"]]
        context_lines.append(
            f"[{cite_num}] Source: {chunk['source_description']}\n{chunk['text']}"
        )
    
    context_block = "\n\n".join(context_lines)
    return f"Context passages:\n\n{context_block}\n\nQuestion: {query}"


def build_sources_md(answer_text: str, chunks: list[dict]) -> str:
    cited_indices = {int(n) for n in re.findall(r"\[(\d+)\]", answer_text)}
    _, unique_sources = get_source_mapping(chunks)
    
    lines = ["**Sources**"]
    for cite_num, desc, url in unique_sources:
        if cite_num in cited_indices:
            lines.append(f"- [{cite_num}] [{desc}]({url})")
            
    if len(lines) == 1:
        return ""
    return "\n".join(lines)


def answer(query: str) -> tuple[str, str]:
    if not query.strip():
        return "", ""

    chunks = retrieve(query, k=TOP_K)

    user_message = build_user_message(query, chunks)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    answer_text = response.choices[0].message.content
    sources_md = build_sources_md(answer_text, chunks)
    return answer_text, sources_md


with gr.Blocks(title="Grinnell CS Unofficial Guide") as demo:
    gr.Markdown("# Grinnell CS Unofficial Guide")
    gr.Markdown(
        "Ask anything about the CS experience at Grinnell — courses, professors, "
        "opportunities, student perspectives."
    )

    with gr.Row():
        query_box = gr.Textbox(
            label="Your question",
            placeholder="e.g. What do students say about Prof Rebelsky?",
            lines=2,
            scale=4,
        )
        submit_btn = gr.Button("Ask", variant="primary", scale=1)

    answer_box = gr.Textbox(label="Answer", lines=10, interactive=False)
    sources_box = gr.Markdown()

    submit_btn.click(fn=answer, inputs=query_box, outputs=[answer_box, sources_box])
    query_box.submit(fn=answer, inputs=query_box, outputs=[answer_box, sources_box])

if __name__ == "__main__":
    demo.launch()
