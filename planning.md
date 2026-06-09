# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

--- The Computer Science experience at Grinnell College, information is really scattered across different sources and perpsectives/opinions, and can be quite confusing to gather for incoming sutdents. 

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | RateMyProfessor | Pr. Osera Review | https://www.ratemyprofessors.com/professor/2063467 |
| 2 | Grinnell Website | Major Requirements | ./documents/CSCourses.txt |
| 3 | RateMyProfessor | Prof Perlmutter | https://www.ratemyprofessors.com/professor/2947551 |
| 4 | RateMyProfessor | Prof Sam Rebelsky | https://www.ratemyprofessors.com/professor/148487 |
| 5 | RateMyProfessor | Prof Curtsinger| https://www.ratemyprofessors.com/professor/2103075 |
| 6 | RateMyProfessor | Prof Weinmann | https://www.ratemyprofessors.com/professor/1349052 |
| 7 | Grinnell Website | Off-Campus Study in CS | https://www.grinnell.edu/academics/majors-concentrations/computer-science/off-campus |
| 8 | Grinnell Website | CS Opportunities | https://www.grinnell.edu/academics/majors-concentrations/computer-science/opportunities |
| 9 | r/Iowa | is Grinnell good for CS? | https://www.reddit.com/r/Iowa/comments/1062qs6/is_grinnell_college_decent_for_comp_sci/ |
| 10 | r/Grinnell | CS at Grinnell | https://www.reddit.com/r/Grinnell/comments/8aeyvl/what_is_the_cs_program_like/ |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 200 

**Overlap:** 30

**Reasoning:** Due to the mix of shorter and longer styled paragraphs between the different types of sources we have (reddit threads and newspaper articles) This felt like a good enough balance.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model: all-MiniLM-L6-v2 via sentence-transformers**

**Top-k: 6**

**Production tradeoff reflection:** I would most probably be weighing in context-length and latency first and foremost; Multilingual support is not a priority due to the college requiring English proficiency to enroll. 

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are the strict limitations regarding taking classes outside of Grinnell College when trying to satisfy the 16 required credits for systems, theory, and software development? | No more thqn 4 credits can be taken out of 16 |
| 2 | For graduation with honors, what roles can i take to fulfill commitment to the department? | Serving on SEPC, working as a peer educator...|
| 3 | I'm moving off-campus next year. Which specific houses or landlords are known for having terrible mold problems?| I don't have the necessary information to answer |
| 4 | Which professor has the best teaching experience with CSC-151 according to students? | Should be Osera or Rebelsky.|
| 5 | Grinnell offers a cooperative Master of Computer Science (M.C.S.) degree. Which university is it partnered with, and when do students need to apply for it? | It is partnered with the University of Iowa and students apply in their second semester of junior year.

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Information split across two different chunks due to differing source structures (reddit thread vs newspaper article)

2. Incorrect/Obsolete information due to some age of the sources.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---
![Document Ingestion Pipeline flow](<Document Ingestion Flow-2026-06-08-123103.png>)

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

I'll describe my document ingestion pipeline to claude, before asking it to implement a function chunk_text() using the specified chunk size and overlap

**Milestone 4 — Embedding and retrieval:**

I will ask Claude to implement an embed function with our chosen embedding model, and storing it within a chromaDB vector database. I will follow it up with a prompt to create a retrieval function.

**Milestone 5 — Generation and interface:**

I will be asking Claude to set up a barebones front-end UI with a chatbox, and connecting said UI to our backend, where our Groq model will retrieve the relevant information to answer with 
