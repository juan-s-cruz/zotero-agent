# Zotero RSS Feed Evaluator & Collector 🤖📚

An automated workspace for native AI agents to check Zotero RSS feed subscriptions, evaluate new papers for relevance to applied machine learning in corporate finance, and file them into targeted Zotero collections.

This setup runs without external Python scripts or code! The agent operates purely on declarative guidelines and leverages the **Model Context Protocol (MCP)** via the **Zotero MCP server** to interface with Zotero.

---

## ✨ Features

- **Automated RSS Feed Monitoring**: Periodically scans Zotero RSS feeds for new academic papers.
- **Smart Relevance Evaluation**: Uses custom heuristic guidelines to filter for high-value research (e.g., applied ML, multivariate forecasting, volatility estimation, SDEs, and synthetic data).
- **Automatic Filing & Organization**: Automatically imports relevant papers directly to a Zotero collection without downloading heavy PDF files (unless requested).
- **Web Insights Expansion**: Supplements academic literature with real-world quantitative/ML industry insights by querying trustworthy blogs (e.g., QuantStart, QuantPedia, Man Group, Two Sigma).
- **Executive Summaries**: Synthesizes findings into a monthly markdown report, complete with a high-level **General Trends & Trajectory** synthesis.

---

## 🏗️ Workspace Structure

- **[.agents/AGENTS.md](.agents/AGENTS.md)**: The core system prompt and instruction manual for the agent. Defines evaluation criteria, goals, and MCP tool instructions.
- **[.agents/mcp_config.json](.agents/mcp_config.json)**: Declarative MCP server configuration containing credentials and configuration for the `zotero-mcp` connection.
- **[.agents/skills/web-news-expander/SKILL.md](.agents/skills/web-news-expander/SKILL.md)**: Guidance rules and targeted sources for expanding searches on industry blogs.
- **[CLAUDE.md](CLAUDE.md)**: Symlink to [.agents/AGENTS.md](.agents/AGENTS.md) for compatibility with Claude Code.
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)**: Symlink to [.agents/AGENTS.md](.agents/AGENTS.md) for compatibility with GitHub Copilot.
- **[.cursorrules](.cursorrules)**: Symlink to [.agents/AGENTS.md](.agents/AGENTS.md) for compatibility with Cursor and other AI-assisted IDEs.
- **[activity/](activity/)**: Output directory containing historical runs, monthly summaries, and synthesized reports.

---

## 🛠️ Configuration & Setup

### 1. Zotero Credentials & Workspace Config

To use this workspace, configure your Zotero credentials and collections by copying the template files and filling in your details:

#### Zotero MCP Server Config

Edit your Zotero credentials in the MCP configuration file [.agents/mcp_config.json](.agents/mcp_config.json) (which is ignored by git):

```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "env": {
        "ZOTERO_LOCAL": "true",
        "ZOTERO_LIBRARY_ID": "YOUR_LIBRARY_ID",
        "ZOTERO_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

- **`ZOTERO_LIBRARY_ID`**: Your Zotero user ID or group library ID.
- **`ZOTERO_API_KEY`**: A personal API key generated from your Zotero account settings.
- **`ZOTERO_LOCAL`**: Set to `"true"` if running a local Zotero instance or proxy.

#### Workspace Collection & Relevance Config

Create a `user_config.json` file in the root of the workspace (using `user_config.json.template` as a model, which is ignored by git) to configure your agent's targets, relevance guidelines, and sources:

```json
{
  "ZOTERO_COLLECTION_KEY": "YOUR_COLLECTION_KEY",
  "ZOTERO_COLLECTION_NAME": "YOUR_COLLECTION_NAME",
  "RESEARCH_TOPIC": "YOUR_RESEARCH_TOPIC (e.g. Applied Machine Learning in Corporate Finance)",
  "RELEVANCE_CRITERIA": {
    "CORE_TOPICS": [
      "Topic 1",
      "Topic 2"
    ],
    "EVALUATION_GUIDELINES": {
      "HIGH_PRIORITY_DIRECT": "Criteria for High Priority papers",
      "MEDIUM_PRIORITY_TRANSFERABLE": "Criteria for Medium Priority papers",
      "LOW_PRIORITY_SKIP": "Criteria for Low Priority papers"
    }
  },
  "TRUSTWORTHY_SOURCES": [
    {
      "name": "Source Name",
      "domain": "domain.com",
      "description": "Short description of the source"
    }
  ],
  "EXAMPLE_SEARCH_QUERIES": [
    "site:domain.com \"query terms\""
  ]
}
```

- **`ZOTERO_COLLECTION_KEY`**: The 8-character Zotero collection key where relevant papers will be saved.
- **`ZOTERO_COLLECTION_NAME`**: The display name of the collection.
- **`RESEARCH_TOPIC`**: The high-level domain or research area for the agent.
- **`RELEVANCE_CRITERIA.CORE_TOPICS`**: Specific topic items the agent should check for relevance during evaluation.
- **`RELEVANCE_CRITERIA.EVALUATION_GUIDELINES`**: Detailed heuristic descriptions mapping to High, Medium, and Low priorities to guide the classification of paper abstracts.
- **`TRUSTWORTHY_SOURCES`**: A list of trusted quant/industry blogs or portals (name, domain, description) that the agent will use for web news expansion.
- **`EXAMPLE_SEARCH_QUERIES`**: Domain-restricted search queries for web news expansion.


#### Initialize the Agent Prompt Instructions

Run the compilation script to inject your custom configuration into the agent's prompt instructions:

```bash
python3 initialize.py
```

This script reads `user_config.json` and compiles the agent's core guidelines in `.agents/AGENTS.md` and `.agents/skills/web-news-expander/SKILL.md` (which are also ignored by git).

### 2. Prerequisites

Make sure the `zotero-mcp` CLI or bridge is installed and accessible in your system's `PATH`.

---

## 🚀 How to Run

1. **Launch the Agent**: Start the Antigravity shell in this directory:

   ```bash
   agy
   ```

2. **Initialize / Inspect**: Run the inspection command inside the workspace session to compile configuration and establish the agent's identity:

   ```bash
   agy inspect
   ```

3. **Trigger the Evaluation**: Run the trigger keyword within the agent session:
   > **get-newsletter**

The agent will automatically execute the entire pipeline:

1. Scan your Zotero RSS feeds.
2. Filter papers using the criteria in [.agents/AGENTS.md](.agents/AGENTS.md).
3. Import relevant titles and URLs to your configured collection (specified in `user_config.json`).
4. Run supplementary web searches via the `web-news-expander` skill.
5. Generate a comprehensive executive summary in `activity/YYYY-MM/YYYY-MM-DD-summary.md`.
