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

#### Workspace Collection Config

Create a `user_config.json` file in the root of the workspace (using `user_config.json.template` as a model, which is also ignored by git) to define the Zotero collection:

```json
{
  "ZOTERO_COLLECTION_KEY": "YOUR_COLLECTION_KEY",
  "ZOTERO_COLLECTION_NAME": "Applied ML - Corp Finance"
}
```

- **`ZOTERO_COLLECTION_KEY`**: The 8-character collection key where relevant papers will be filed.
- **`ZOTERO_COLLECTION_NAME`**: The display name of the collection.

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
