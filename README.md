# Zotero RSS Feed Evaluator & Collector 🤖📚

An automated workspace for native AI agents to check Zotero RSS feed subscriptions, evaluate new papers for relevance to applied machine learning in corporate finance, and file them into targeted Zotero collections.

The agent operates on declarative guidelines, leveraging the **Model Context Protocol (MCP)** to interface with Zotero and automated python scripts to manage workspace dependencies and Zotero report persistence.

---

## ✨ Features

- **Automated RSS Feed Monitoring**: Periodically scans Zotero RSS feeds for new academic papers.
- **Smart Relevance Evaluation**: Uses custom heuristic guidelines to filter for high-value research (e.g., applied ML, multivariate forecasting, volatility estimation, SDEs, and synthetic data).
- **Automatic Filing & Organization**: Automatically imports relevant papers directly to a Zotero collection without downloading heavy PDF files (unless requested).
- **Web Insights Expansion**: Supplements academic literature with real-world quantitative/ML industry insights by querying trustworthy blogs (e.g., QuantStart, QuantPedia, Man Group, Two Sigma).
- **Executive Summaries**: Synthesizes findings into a markdown report, featuring a high-level **General Trends & Trajectory** synthesis.
- **Automated Newsletter Persistence**: Immediately pushes the compiled report as a Parent Report item and attached Child Note (HTML format) to the user's Zotero newsletters collection via a dedicated subagent.

---

## 🏗️ Workspace Structure

- **[.agents/AGENTS.md](.agents/AGENTS.md)**: The core system prompt and instruction manual for the agent. Defines evaluation criteria, goals, and MCP tool instructions.
- **[.agents/mcp_config.json](.agents/mcp_config.json)**: Declarative MCP server configuration containing credentials and configuration for the `zotero-mcp` connection.
- **[.agents/skills/web-news-expander/SKILL.md](.agents/skills/web-news-expander/SKILL.md)**: Guidance rules and targeted sources for expanding searches on industry blogs.
- **[.agents/skills/newsletter-persister/SKILL.md](.agents/skills/newsletter-persister/SKILL.md)**: Guidelines for the subagent responsible for publishing reports back to Zotero.
- **[.agents/skills/newsletter-persister/scripts/persist.py](.agents/skills/newsletter-persister/scripts/persist.py)**: Python script to convert markdown summaries to HTML and push them to Zotero.
- **[CLAUDE.md](CLAUDE.md)**: Symlink to [.agents/AGENTS.md](.agents/AGENTS.md) for compatibility with Claude Code.
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)**: Symlink to [.agents/AGENTS.md](.agents/AGENTS.md) for compatibility with GitHub Copilot.
- **[.cursorrules](.cursorrules)**: Symlink to [.agents/AGENTS.md](.agents/AGENTS.md) for compatibility with Cursor and other AI-assisted IDEs.
- **[activity/](activity/)**: Output directory containing historical runs, summaries, and synthesized reports.
- **[requirements.txt](requirements.txt)**: List of Python packages required by the workspace scripts.

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

- **`ZOTERO_LIBRARY_ID`**: Your Zotero User ID (for personal libraries) or Group ID (for group libraries). You can find your personal User ID on the [Zotero API Settings page](https://www.zotero.org/settings/keys) under "Your userID for use in API calls". For group libraries, the Group ID is the numeric ID found in the URL when viewing the group library page on zotero.org (e.g., `zotero.org/groups/123456/items`).
- **`ZOTERO_API_KEY`**: A personal private key generated from your [Zotero API Settings page](https://www.zotero.org/settings/keys) under "Create new private key".
- **`ZOTERO_LOCAL`**: Set to `"true"` if running a local Zotero instance or proxy.

#### How the MCP Server Connects

The `zotero-mcp` server is what the agent actually calls (`zotero_get_feed_items`, `zotero_add_by_url`, etc.) — it's a bridge between the agent and Zotero, not Zotero itself.

- With `ZOTERO_LOCAL=true`, the server talks to the **Zotero desktop app's local HTTP API** on this machine, not zotero.org. **Zotero desktop must be running** for any `zotero_*` tool call to succeed. Enable local API access once in Zotero: Settings → Advanced → "Allow other applications on this computer to communicate with Zotero".
- With `ZOTERO_LOCAL` unset/`false`, the server instead calls the Zotero **web API**, and `ZOTERO_API_KEY`/`ZOTERO_LIBRARY_ID` are used for real authentication.
- If every Zotero tool call fails with a connection error, check Zotero desktop is open before checking credentials.

#### Workspace Collection & Relevance Config

Create a `user_config.json` file in the root of the workspace (using `user_config.json.template` as a model, which is ignored by git) to configure your agent's targets, relevance guidelines, and sources:

```json
{
  "ZOTERO_COLLECTION_KEY": "YOUR_COLLECTION_KEY",
  "ZOTERO_COLLECTION_NAME": "YOUR_COLLECTION_NAME",
  "NEWSLETTERS_COLLECTION_KEY": "YOUR_NEWSLETTERS_COLLECTION_KEY",
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

- **`ZOTERO_COLLECTION_KEY`**: The 8-character alphanumeric collection key where relevant papers will be saved. To find it, open the collection in your web browser on zotero.org; the key is the last part of the URL path (e.g., `zotero.org/users/123456/collections/B2KQMPNI`).
- **`ZOTERO_COLLECTION_NAME`**: The display name of the papers collection (e.g., "Applied ML - Corp Finance").
- **`NEWSLETTERS_COLLECTION_KEY`**: The 8-character alphanumeric collection key where the compiled newsletters reports should be saved. Find this key in the Zotero collection URL in the same manner as the `ZOTERO_COLLECTION_KEY` (e.g., `zotero.org/users/123456/collections/E63WSRX2`).
- **`RESEARCH_TOPIC`**: The high-level domain or research area for the agent.
- **`RELEVANCE_CRITERIA.CORE_TOPICS`**: Specific topic items the agent should check for relevance during evaluation.
- **`RELEVANCE_CRITERIA.EVALUATION_GUIDELINES`**: Detailed heuristic descriptions mapping to High, Medium, and Low priorities to guide the classification of paper abstracts.
- **`TRUSTWORTHY_SOURCES`**: A list of trusted quant/industry blogs or portals (name, domain, description) that the agent will use for web news expansion.
- **`EXAMPLE_SEARCH_QUERIES`**: Domain-restricted search queries for web news expansion.

#### Initialize the Agent Prompt Instructions & Environment

Run the initialization script to compile your configuration into the agent's instructions, set up the local virtual environment `.venv`, and install the required workspace dependencies:

```bash
python3 initialize.py
```

This script automatically:

1. Creates a local Python virtual environment `.venv` at the workspace root if it does not already exist.
2. Installs/updates the required Python packages (such as `markdown` for converting summaries to Zotero-friendly HTML) inside the `.venv` from `requirements.txt`.
3. Reads `user_config.json` and compiles the agent's core instructions in `.agents/AGENTS.md` and `.agents/skills/web-news-expander/SKILL.md` (which are both ignored by git).

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
6. Invoke the `newsletter-persister` subagent to convert the summary to HTML and push it to your configured newsletters collection in Zotero.
