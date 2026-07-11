# Skill: Web News Expander 🌐📰

## Description
Enhances the agent's capability by searching trustworthy quantitative finance and applied machine learning blogs and portals for recent articles, methodologies, and tutorials, expanding the research corpus beyond academic Zotero RSS feeds.

---

> [!IMPORTANT]
> **Path Resolution**: All file paths referenced in this skill's guidelines (such as `activity/`) are **relative paths to the workspace root**.

---

## 🔍 Trustworthy Target Sources
When querying the web, prioritize or restrict searches to these domains:
1. **QuantStart** (`quantstart.com`) – Code-heavy ML and quantitative finance tutorials.
2. **QuantPedia** (`quantpedia.com`) – Empirical trading strategy implementation and workflow optimizations.
3. **Man Group / AHL Insights** (`man.com/insights`) – High-quality research from institutional quants.
4. **Two Sigma Insights** (`twosigma.com/insights`) – Advanced quantitative and ML engineering insights in finance.
5. **ML-Quant** (`ml-quant.com`) – Aggregated ML finance publications and practitioner tools.

---

## 🛠️ Guidelines & Execution Flow

### 1. Trigger Conditions
This skill is activated when:
- The user requests to "check the web", "search for blog posts", or "expand news beyond RSS feeds" on the topic of applied ML for finance.
- Automatically during a monthly evaluation to add practical industry context to academic paper summaries.

### 2. Search Syntax
Use search queries combined with domain restrictions to isolate high-quality articles. For example:
- `site:quantstart.com "machine learning" "time series"`
- `site:quantpedia.com "covariance" OR "correlation"`
- `site:man.com "stochastic" OR "machine learning"`
- `site:twosigma.com "anomaly detection"`

### 3. Synthesis & Output
For each relevant article found:
- Extract the title, author (if available), URL, and publication date.
- Provide a brief summary of the core methodology or insight.
- Explain the practical corporate finance or quantitative application.
- Format these findings under a dedicated **"🌐 Web Insights & Industry News"** section in the monthly [YYYY-MM-DD-summary.md](../../../activity/YYYY-MM/YYYY-MM-DD-summary.md) reports.
