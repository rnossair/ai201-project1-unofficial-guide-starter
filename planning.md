# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

--- Grinnell Dorm Culture and Self Governance, information is really scattered across different sources and perpsectives/opinions, and its an integral part of life on campus

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/Grinnell | What are dorms like? | https://www.reddit.com/r/Grinnell/comments/n4po1g/what_are_the_different_dorm_buildings_on_campus/ |
| 2 | Grinnell Website | Self Gov 101 | https://www.grinnell.edu/news/self-gov-101 |
| 3 | Grinnell Website | Self Defining Self Governance | https://www.grinnell.edu/news/self-defining-self-governance |
| 4 | Scarlet & Black (Student Newspaper) | | https://thesandb.com/39417/article/self-gov-is-dead-did-it-ever-exist-anyway/ |
| 5 | Grinnell Student Handbook | Self Gov at Grinnell| https://catalog.grinnell.edu/content.php?catoid=32&navoid=5205#self-governance_at_grinnell_college |
| 6 | Grinnell Website | Residence Halls | https://www.grinnell.edu/campus-life/student-life/living-spaces/residence-halls |
| 7 | r/Grinnell | Social life @ Grinnell | https://www.reddit.com/r/Grinnell/comments/xgbnuo/hows_the_social_life/ |
| 8 | Grinnell Website | Student Organization | https://www.grinnell.edu/life/organizations |
| 9 | Scarlet & Black (Student Newspaper) | Nightlife at Grinnell | https://thesandb.com/38899/article/nightlife-in-the-prairie/ |
| 10 | Scarlet & Black (Student Newspaper) | Different vibes of each campus cluster | https://thesandb.com/46692/article/student-speaks-dorm-hall-defense/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**250

**Overlap:**50

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
| 1 | What do students think about activities in town? | Town doesn't have much to do but there are organizations on campus|
| 2 | What campus should I live on if i value quiet? | East campus is known as the quietest.|
| 3 | I'm moving off-campus next year. Which specific houses or landlords are known for having terrible mold problems?| I don't have the necessary information to answer|
| 4 | I'm not really into loud drinking parties and I know we don't have Greek life. If I live in one of the quieter dorms, is it still easy to find a solid community here, or does the social scene end up feeling really isolating? | It is definitely possible to find a solid community, but it requires a bit of deliberate effort.|
| 5 | I'm trying to figure out the party scene before I commit. Which fraternities or sororities are the best to join at Grinnell, and where are their houses located? | Grinnell has no greek life. |

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
![Document Ingestion Pipeline flow](<Document Ingestion Flow-2026-06-07-235643.png>)

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
