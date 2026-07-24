import os
import sys
import json
import subprocess


def main():
    config_path = "user_config.json"
    if not os.path.exists(config_path):
        print(
            f"Error: {config_path} not found. Please create it first by copying user_config.json.template."
        )
        return

    # 1. Ensure virtual environment exists
    venv_dir = ".venv"
    venv_python = (
        os.path.join(venv_dir, "Scripts", "python.exe")
        if os.name == "nt"
        else os.path.join(venv_dir, "bin", "python")
    )

    if not os.path.exists(venv_dir):
        print("Creating virtual environment (.venv)...")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            print("Virtual environment created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            return
    else:
        print("Virtual environment (.venv) already exists.")

    # 2. Ensure dependencies are installed
    requirements_path = "requirements.txt"
    if os.path.exists(requirements_path):
        print("Installing/updating dependencies in .venv from requirements.txt...")
        try:
            subprocess.run(
                [venv_python, "-m", "pip", "install", "-r", requirements_path],
                check=True,
            )
            print("Dependencies successfully installed.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            return

    print("Reading configuration...")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 3. Prepare replacements
    replacements = {
        "RESEARCH_TOPIC": config.get("RESEARCH_TOPIC", ""),
        "ZOTERO_COLLECTION_NAME": config.get("ZOTERO_COLLECTION_NAME", ""),
        "ZOTERO_COLLECTION_KEY": config.get("ZOTERO_COLLECTION_KEY", ""),
        "NEWSLETTERS_COLLECTION_KEY": config.get("NEWSLETTERS_COLLECTION_KEY", ""),
        "ZOTERO_LIBRARY_ID": config.get("ZOTERO_LIBRARY_ID", ""),
    }

    # Format CORE_TOPICS as markdown list items
    core_topics = config.get("RELEVANCE_CRITERIA", {}).get("CORE_TOPICS", [])
    replacements["CORE_TOPICS"] = "\n".join([f"   - {topic}" for topic in core_topics])

    # Format TRUSTWORTHY_SOURCES as numbered list items for SKILL.md
    sources = config.get("TRUSTWORTHY_SOURCES", [])
    replacements["TRUSTWORTHY_SOURCES_LIST"] = "\n".join(
        [
            f"{i}. **{s.get('name')}** (`{s.get('domain')}`) – {s.get('description')}"
            for i, s in enumerate(sources, 1)
        ]
    )

    # Format EXAMPLE_SEARCH_QUERIES as markdown list items for SKILL.md
    queries = config.get("EXAMPLE_SEARCH_QUERIES", [])
    replacements["EXAMPLE_SEARCH_QUERIES_LIST"] = "\n".join(
        [f"- `{query}`" for query in queries]
    )

    # Evaluation Guidelines
    guidelines = config.get("RELEVANCE_CRITERIA", {}).get("EVALUATION_GUIDELINES", {})
    replacements["HIGH_PRIORITY_DIRECT"] = guidelines.get("HIGH_PRIORITY_DIRECT", "")
    replacements["MEDIUM_PRIORITY_TRANSFERABLE"] = guidelines.get(
        "MEDIUM_PRIORITY_TRANSFERABLE", ""
    )
    replacements["LOW_PRIORITY_SKIP"] = guidelines.get("LOW_PRIORITY_SKIP", "")

    # 4. Process templates
    templates = [
        (".agents/AGENTS.md.template", ".agents/AGENTS.md"),
        (
            ".agents/skills/web-news-expander/SKILL.md.template",
            ".agents/skills/web-news-expander/SKILL.md",
        ),
        (
            ".agents/skills/newsletter-persister/SKILL.md.template",
            ".agents/skills/newsletter-persister/SKILL.md",
        ),
    ]

    for template_path, target_path in templates:
        if not os.path.exists(template_path):
            print(f"Error: Template {template_path} not found.")
            continue

        print(f"Processing template {template_path} -> {target_path}...")
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        for placeholder, value in replacements.items():
            content = content.replace(f"{{{{{placeholder}}}}}", str(value))

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

    print("Agent system successfully initialized!")


if __name__ == "__main__":
    main()
