# Skill: Web News Expander 🌐📰

## Description
Enhances the agent's capability by searching trustworthy blogs and portals for recent articles, methodologies, and tutorials, expanding the research corpus beyond academic Zotero RSS feeds.

---

> [!IMPORTANT]
> **Path Resolution**: All file paths referenced in this skill's guidelines (such as `activity/`) are **relative paths to the workspace root**.

---

## 🔍 Trustworthy Target Sources
When querying the web, read and prioritize the list of domains and descriptions specified in the `user_config.json` configuration file at the root of the workspace under `TRUSTWORTHY_SOURCES`.

---

## 🛠️ Guidelines & Execution Flow

### 1. Trigger Conditions
This skill is activated when:
- The user requests to "check the web", "search for blog posts", or "expand news beyond RSS feeds" on the target topic of interest.
- Automatically during a weekly/monthly evaluation to add practical industry context to academic paper summaries.

### 2. Search Syntax
Read and use the search syntax guidelines and queries defined in the `user_config.json` configuration file at the root of the workspace under `EXAMPLE_SEARCH_QUERIES`. Make sure to combine search terms with the trustworthy target domains to isolate high-quality articles.

### 3. Synthesis & Output
For each relevant article found:
- Extract the title, author (if available), URL, and publication date.
- Provide a brief summary of the core methodology or insight.
- Explain the practical application to the target topic (`RESEARCH_TOPIC` from `user_config.json`).
- Format these findings under a dedicated **"🌐 Web Insights & Industry News"** section in the [YYYY-MM-DD-summary.md](../../../activity/YYYY-MM/YYYY-MM-DD-summary.md) reports.

