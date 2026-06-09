# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This system covers the **Computer Science experience at Grinnell College** which includes major requirements, professor reviews, major opportunities and policies, and student perspectives on the program's culture and difficulty.

This knowledge is valuable because official sources (the course catalog, department website) describe requirements and course titles but say almost nothing about what courses actually feel like, which professors are most supportive, or how students navigate the program in practice. That lived knowledge is scattered across Reddit threads, RateMyProfessor reviews, and word-of-mouth, making it hard for prospective or incoming students to build a realistic picture.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | RateMyProfessor | Professor reviews | https://www.ratemyprofessors.com/professor/2063467 |
| 2 | Grinnell Website | CS Major Requirements (local file) | `documents/CSCourses.txt` taken from https://www.grinnell.edu/academics/majors-concentrations/computer-science/major |
| 3 | RateMyProfessor | Professor reviews | https://www.ratemyprofessors.com/professor/2947551 |
| 4 | RateMyProfessor | Professor reviews | https://www.ratemyprofessors.com/professor/148487 |
| 5 | RateMyProfessor | Professor reviews | https://www.ratemyprofessors.com/professor/2103075 |
| 6 | RateMyProfessor | Professor reviews | https://www.ratemyprofessors.com/professor/1349052 |
| 7 | Grinnell Website | Off-Campus Study in CS | https://www.grinnell.edu/academics/majors-concentrations/computer-science/off-campus |
| 8 | Grinnell Website | CS Opportunities | https://www.grinnell.edu/academics/majors-concentrations/computer-science/opportunities |
| 9 | r/Iowa | "Is Grinnell good for comp sci?" thread | https://www.reddit.com/r/Iowa/comments/1062qs6/is_grinnell_college_decent_for_comp_sci/ |
| 10 | r/Grinnell | "What is the CS program like?" thread | https://www.reddit.com/r/Grinnell/comments/8aeyvl/what_is_the_cs_program_like/ |
| 11 | explorebestcolleges | CS at Grinnell Overview (local file) | `documents/explorebestcolleges.txt` taken from https://www.explorebestcolleges.com/degrees/l/24262/grinnell-college-computer-science-bachelors-degree |

---

## Chunking Strategy

**Chunk size:** 1000 characters

**Overlap:** 150 characters

**Why these choices fit your documents:**

Our sources mixes two structurally different document types. RateMyProfessor pages consist of short, self-contained review paragraphs (typically 50–200 characters each), while the Grinnell website pages contain multi-paragraph policy prose. A 1000-character window is wide enough to hold 2–4 complete professor reviews or a full policy paragraph, while staying well under the 256-token input limit of the embedding model.

The splitter used is LangChain's `RecursiveCharacterTextSplitter` with separators `["\n\n", "\n", ".", " ", ""]`. This ordering matters: `fetch_rmp` joins individual reviews with `"\n\n"`, so the splitter's first separator naturally keeps each review intact as a unit before falling back to sentence or word boundaries. A plain word-counting chunker cannot respect these structural boundaries.

The 150-character overlap prevents a sentence from being cut exactly at a chunk boundary, ensuring that semantically related content spanning two chunks has some representation in both.

**Final chunk count:** 54 chunks across all 11 sources (sources 2 and 11 are local `.txt` files).

---

## Sample Chunks

**Chunk 1 — `src1_chunk0` | RateMyProfessor: Prof Osera Review**
```
Course: CSC151. Review: PM is awesome. CS-151 is a really not fun experience in general but he makes
it more than bearable.

Course: CSC151. Review: Osera is a great professor to have for CSC-151 because he wrote the language
that the class is taught in. By the third semester of this language there shouldn't be many bugs, but
it is nice to have access to someone who understands what is going on and can help you debug.
```

**Chunk 2 — `src2_chunk3` | Grinnell Website: Major Requirements**
```
Major Requirements: A minimum of 32 credits
Multi-paradigm, Introductory Sequence: 12 credits
  CSC 151 - Functional Problem Solving with Lab
  CSC 161 - Imperative Problem Solving with Lab
  CSC 207 - Object-Oriented Problem Solving, Data Structures, and Algorithms
Systems: 4 credits required, 8 credits recommended
  CSC 211 - Computer Organization and Architecture
  or CSC 213 - Operating Systems and Parallel Computing
```

**Chunk 3 — `src4_chunk0` | RateMyProfessor: Prof Sam Rebelsky**
```
Course: CSC151. Review: I absolutely adore the token system and mastery-based learning! Class was more
work than I expected, but manageable. He cares about students and gives good feedback and banter. His
tangents make the mornings better :)

Course: CSC151. Review: Sam is extremely kind and he built a fun communal environment in his classroom
that I would never have expected from a CS class.
```

**Chunk 4 — `src7_chunk4` | Grinnell Website: Off-Campus Study in CS**
```
Some programs have areas of particular strength. For example, AIT-Budapest emphasizes theory and
innovation, with some courses taught by top mathematicians or seasoned entrepreneurs. Australia's
university system emphasizes preparation for professional practice, with some courses taught by
professional software engineers. If you or your advisor can identify such a strength, you should take
advantage of it.
```

**Chunk 5 — `src9_chunk3` | r/Iowa: is Grinnell good for CS?**
```
Hey mate. A recent graduate from Grinnell interned in my job's IT department (application developers).
Since I was involved in the internship experience, I got to know him pretty well. He was an
international student and he said he really liked Grinnell's program. Graduated and immediately landed
a job in Dallas, TX. With Des Moines semi-close, tons of internship opportunities with awesome
internship programs.
```

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` (local, no API required)

**Production tradeoff reflection:**

For a real deployment, the main tradeoffs to weigh would be **context length** and **retrieval accuracy**. `all-MiniLM-L6-v2` has a 256-token max input, meaning longer chunks get silently truncated, which we might need to replace for longer chunks. On accuracy, `all-MiniLM-L6-v2` is a general-purpose model and doesn't have specific training on academic or CS domain text, a fine-tuned model would likely rank professor reviews more precisely. Multilingual support is not a priority here since Grinnell requires English proficiency.

---

## Retrieval Test Results

### Query 1: "What do students think of Prof Rebelsky?"

| Rank | Score (cosine dist.) | Source |
|------|---------------------|--------|
| 1 | 1.1382 | RateMyProfessor: Prof Sam Rebelsky |
| 2 | 1.2841 | RateMyProfessor: Prof Osera Review |
| 3 | 1.3080 | RateMyProfessor: Prof Osera Review |
| 4 | 1.3505 | RateMyProfessor: Prof Sam Rebelsky |

**Top chunk snippet:** *"...Sam cares about his students and wants to see you understand the material. He gives you multiple opportunities to showcase you understand the learning assessment so don't feel stressed..."*

**Why these results are relevant:** Ranks 1 and 4 are both Rebelsky chunks — a direct match. Ranks 2 and 3 are two Osera chunks, retrieved because all RMP pages share the same structure: short informal review paragraphs mentioning the same course codes (CSC151, CSC208). The embedding model cannot sharply distinguish between professor pages on name alone when the surrounding prose is structurally identical.

---

### Query 2: "What are the CS major requirements at Grinnell?"

| Rank | Score (cosine dist.) | Source |
|------|---------------------|--------|
| 1 | 0.6689 | Grinnell Website: Off-Campus Study in CS |
| 2 | 0.7111 | Grinnell Website: Major Requirements |
| 3 | 0.7426 | Grinnell Website: Major Requirements |
| 4 | 0.7494 | r/Iowa: is Grinnell good for CS? |

**Top chunk snippet:** *".... Some programs have areas of particular strength. For example, AIT-Budapest emphasizes theory and innovation, with some courses taught by top mathematicians or seasoned entrepreneurs. Australia's uni..."*

**Why these results are relevant:** The off-campus study page explicitly discusses whether transfer courses can "satisfy major requirements" and uses the exact phrase repeatedly in the context of credit approval, making it semantically close despite not being the primary requirements document. The correct source on major requirements (CSCourses.txt) ranks second.

---

### Query 3: "Is Grinnell good for computer science?"

| Rank | Score (cosine dist.) | Source |
|------|---------------------|--------|
| 1 | 0.6536 | explorebestcolleges: CS at Grinnell Overview |
| 2 | 0.7268 | explorebestcolleges: CS at Grinnell Overview |
| 3 | 0.7281 | explorebestcolleges: CS at Grinnell Overview |
| 4 | 0.7767 | Grinnell Website: Off-Campus Study in CS |

**Top chunk snippet:** *"...The curriculum includes core courses in programming, data structures, algorithms, computer architecture, and software engineering, along with electives that cover topics such as artificial intelligence and machine learning..."*

**Why these results are relevant:** The top three results are all explorebestcolleges chunks, which directly cover Grinnell's CS bachelor's degree — curriculum overview, career prospects, and institutional stats. Rank 4 (off-campus study page) is pulled in because it discusses CS course quality and program strengths, which overlaps semantically with a broad program-quality query.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are a helpful assistant that answers questions about the Computer Science \
experience at Grinnell College.

Rules you must follow:
1. Base your answer ONLY on the context passages in the provided documents. \
Do not use outside knowledge.
2. Cite every factual claim by mentioning the file name or url associated with the entry, this is non-negotiable.
3. When citing, use the format [1], [2], etc. corresponding to the numbered context SOURCES. If two passage are from the same source, they share the same number. \
4. If the context does not contain enough information to answer, say so clearly \
instead of guessing.
5. Be concise and direct.
```

**How source attribution is surfaced in the response:**

Each retrieved chunk is prepended with a number `[1]`–`[6]` and its source label before being sent to the model. After the model responds, the app parses citation numbers from the answer text and displays only the corresponding sources as clickable links.

---

## Example Responses

### Response 1 — In-scope with policy citation

**Query:** *What are the strict limitations on taking classes outside of Grinnell to satisfy the 16 required credits for systems, theory, and software development?*

**Response:**
> According to the Grinnell Website: Major Requirements [1], "No more than 4 credits taken outside of Grinnell may be counted towards the 16 required credits for systems, upper-level theory, and software development." This indicates that students can take a limited number of credits outside of Grinnell to satisfy these requirements, with a maximum of 4 credits allowed.
>
> **Sources**
> - [1] [Grinnell Website: Major Requirements](documents/CSCourses.txt)

---

### Response 2 — In-scope with student-voice citation

**Query:** *What do students say about taking CSC 151 with Prof Rebelsky?*

**Response:**
> According to the context passage [1], students say that they "loved" taking CSC151 with Prof Rebelsky. They mention that the class has a unique grading/token system, but it is clear with grade expectations. They also appreciate that Prof Rebelsky is "incredibly caring and accommodating". Although the class is not easy and requires spending hours on MPs (machine problems), students feel that it is worth it.
>
> **Sources**
> - [1] [RateMyProfessor: Prof Sam Rebelsky](https://www.ratemyprofessors.com/professor/148487)

---

### Response 3 — Out-of-scope refusal

**Query:** *I am moving off-campus next year. Which specific houses or landlords are known for having terrible mold problems?*

**Response:**
> The context passages do not contain enough information to answer your question about specific houses or landlords with terrible mold problems [1], [2]. The passages primarily discuss the Computer Science experience at Grinnell College, its reputation, and comparisons with other colleges, but do not mention anything about off-campus housing or mold problems.
---

## Query Interface

The app is a Gradio web UI. To launch it:

```
.venv\Scripts\python.exe app.py
```

Then open `http://127.0.0.1:7862` in your browser.

**Input fields:**
- **Your question** — a free-text box for the user to input their question.

**Output fields:**
- **Answer** — the LLM's grounded response with inline citations.
- **Sources** — List of every cited source with a clickable link, numbered to match the inline citations.

**Sample interaction transcript:**

**Query: What are the requirements for graduations with honors?**

**Response:**

> To be considered for honors in computer science, graduating seniors must meet the College's general requirements for honors and demonstrate exceptional commitment to the discipline and its values [1]. The Department considers students' work in four areas: 
> 1. Excellence in the classroom, which can be satisfied by meeting the College's GPA requirement for honors [1].
> 2. Excellence beyond the classroom, demonstrated through work completed during a MAP, internship, research experience, or other impactful project, which is presented at a poster session [1].
> 3. Commitment to the department, shown by serving on SEPC, working as a peer educator, mentoring students, or taking on other official roles [1].
> 4. Commitment to the discipline, demonstrated by taking more than the minimal computer science major courses, although this requirement may be waived due to enrollment pressures [1].
>
> **Sources:**
>
> - [1] Grinnell Website: Major Requirements (./documents/CSCourses.txt)

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are the strict limitations on taking classes outside Grinnell to satisfy the 16 required systems/theory/software credits? | No more than 4 credits can be taken outside Grinnell | Correctly cited the 4-credit cap with direct attribution to CSCourses.txt | Relevant | Accurate |
| 2 | For graduation with honors, what roles can I take to fulfill commitment to the department? | Serving on SEPC, working as a peer educator, etc. | Correctly retrieved and summarized the honors commitment roles from the major requirements document | Relevant | Accurate |
| 3 | I'm moving off-campus. Which specific landlords are known for terrible mold problems? | I don't have the necessary information to answer | Correctly refused and directed user to external resources | N/A (out of scope) | Accurate |
| 4 | Which professor has the best teaching experience with CSC-151 according to students? | Prof. Sam Rebelsky has the majority of positive reviews, as well as Prof. Osera | Correctly retrieved student reviews for Professors teaching CSC-151 | Relevant | Accurate |
| 5 | Grinnell offers a cooperative M.C.S. degree — which university is it partnered with, and when do students apply? | University of Iowa; apply in second semester of junior year | Correctly retrieved from CS Opportunities page; cited U of Iowa partnership and junior-year application window | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** *"What do students think of Prof Rebelsky?"*

**What the system returned:** The correct Rebelsky RateMyProfessor page ranked first, but ranks 2 and 3 were the two Osera RMP chunks, which were unrelated to the query.

**Root cause (tied to a specific pipeline stage):** The failure is in the embedding + retrieval stage. All five RateMyProfessor pages are structurally identical, mentioning course codes like CSC151 and informal CS vocabulary, which explains how the embedding model encodes each page into a very similar region of the vector space. Because the query ("Prof Rebelsky") is short and the professor's name appears sparsely in chunks (only at review headers, which the splitter may push to the edge of a chunk), the model cannot reliably distinguish between specific professor reviews. The distances between the top 3 results are close: 1.14, 1.28, 1.31: too small of a margin to filter noise.

**What you would change to fix it:** In `fetch_rmp`, prepend the professor's full name to each review block before chunking, e.g. `"Professor: Sam Rebelsky\nCourse: CSC151. Review: ..."`. This would anchor each chunk more explicitly to its subject, giving the embedding model a stronger signal to differentiate between professor pages. We could also implement keyword search (BM25) to help provide more relevant results.

---

## Spec Reflection

**One way the spec helped you during implementation:**

The planning.md spec required listing all 11 sources with specific URLs and source types before writing any pipeline code, which helped me form an idea of the chunking strategy I would pick. This also forced me to pick information fetchers for the ingesting phase: two specialized fetchers and a general web fetcher(`fetch_rmp`, `fetch_reddit`, `fetch_web`) plus two local file readers (`fetch_txt`, `fetch_pdf`) were needed.

**One way your implementation diverged from the spec, and why:**

The spec specified a word-based chunker with `chunk_size=200 words` and `overlap=30 words`. During implementation this was replaced with LangChain's `RecursiveCharacterTextSplitter` at `chunk_size=1000 characters` / `overlap=150 characters`. The reason: RateMyProfessor reviews are discrete units separated by double newlines (`\n\n`), and a word-counting splitter has no mechanism to respect those boundaries. The recursive character splitter, with `"\n\n"` as its first separator, keeps each review intact before falling back to finer boundaries.

---

## AI Usage

**Instance 1 — Implementing the ingestion pipeline**

- *What I gave the AI:* I asked Claude to write an ingestion script capable of loading documents, properly cleaning them, and chunking them according to the specified chunk size and overlap chosen in the planning.md doc.
- *What it produced:* Claude generated the full `ingest.py` with `fetch_web`, `fetch_reddit`, `fetch_pdf`, `clean_text`, and `chunk_text` functions, along with a `SOURCES` list and a `main()` that writes all chunks to `documents/chunks.json`. It also added `beautifulsoup4` and `requests` to `requirements.txt`, both necessary for web scraping.
- *What I changed or overrode:* I overrode the source-specific scraping for Scarlet & Black by asking Claude to target only the `#sno-story-body-content` element, and separately directed it to use `#siteTable` and `.commentarea` for Reddit instead of the broader selectors it had generated, both choices taken to minimize the amount of noise found in navigation headers and ads. 

**Instance 2 — Building the Gradio frontend**

- *What I gave the AI:* I asked Claude to build a front-end ui built on top of gradio, specifically asking it to connect Groq's `llama-3.3-70b-versatile` model to our chromaDB vector database. I additionally asked it to make sure the LLM system prompt kept the model grounded on only the provided documents, while ensuring proper citation.
- *What it produced:* Claude generated `app.py` with a `build_user_message` function that numbers each chunk `[1]`–`[6]`, a system prompt enforcing citation and grounding rules, a Groq API call, and a Gradio layout with a query box, answer box, and sources list.
- *What I changed or overrode:* I made a few changes to the system prompt that I believed would assist in ensuring an appropriate response. I also directed Claude to adjust `build_sources_md` so that only sources actually cited in the LLM's response appear in the sources panel, rather than listing all retrieved chunks.

