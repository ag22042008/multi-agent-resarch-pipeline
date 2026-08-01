# 🖋️ Inkling — Multi-Agent Research Pipeline

> *a small idea, researched into a full one*

Inkling turns a single topic into a fully researched, fact-checked report — no manual searching, reading, or drafting required. Give it a topic, and four specialized AI agents take it from there: one searches, one reads, one writes, and one critiques.

---

## How it works

Inkling isn't one model doing everything — it's four agents handing work off to each other, each with a single job:

| Step | Agent | Job |
|------|-------|-----|
| 01 | **Search** | Finds recent, reliable sources on the topic |
| 02 | **Read** | Picks the most relevant source and scrapes it for depth |
| 03 | **Write** | Drafts a structured report from the combined research |
| 04 | **Critique** | Reviews the report and flags gaps or weak claims |

The full shared state (search results, scraped content, report, and feedback) is returned at the end, so nothing along the way is thrown away.

## Tech stack

- **LLM reasoning** — [Mistral AI](https://mistral.ai/) via `langchain-mistralai`
- **Agent orchestration** — [LangGraph](https://github.com/langchain-ai/langgraph) / LangChain
- **Web search** — [Tavily](https://tavily.com/)
- **Content extraction** — `requests` + `BeautifulSoup`
- **UI** — [Streamlit](https://streamlit.io/)

## Project structure

```
.
├── agents.py           # Search/reader agents + writer/critic chains
├── main_pipeline.py     # Orchestrates the 4-step pipeline
├── tools.py              # Tool definitions used by the agents
├── app.py               # Streamlit UI ("Inkling")
├── requirements.txt
└── .env                  # API keys (not committed)
```

## Getting started

### Prerequisites

- Python 3.10+
- A [Mistral AI](https://console.mistral.ai/) API key
- A [Tavily](https://app.tavily.com/) API key

### Installation

```bash
git clone <your-repo-url>
cd multi-agent-resarch-pipeline
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_key_here
TAVILY_API_KEY=your_tavily_key_here
```

> Deploying on Streamlit Cloud instead? Add the same two keys under **Settings → Secrets** in TOML format.

### Usage

**Streamlit UI:**

```bash
streamlit run app.py
```

**Or run the pipeline directly from the CLI:**

```bash
python main_pipeline.py
```

You'll be prompted for a topic, and the full pipeline (search → read → write → critique) will run in your terminal.

## Roadmap

- [ ] Stream live per-agent progress instead of a single blocking run
- [ ] Support multiple scraped sources per report, not just one
- [ ] One-click export to PDF/Word
- [ ] Swap in alternate LLM providers

## License

MIT — feel free to fork and adapt.

## Author

Built by **[Your Name]** — [GitHub](#) · [LinkedIn](#)
