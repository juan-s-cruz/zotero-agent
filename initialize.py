import os
import json

def main():
    config_path = 'user_config.json'
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found. Please create it first by copying user_config.json.template.")
        return

    print("Reading configuration...")
    with open(config_path, 'r') as f:
        config = json.load(f)

    # 1. Prepare replacements
    replacements = {
        'RESEARCH_TOPIC': config.get('RESEARCH_TOPIC', ''),
        'ZOTERO_COLLECTION_NAME': config.get('ZOTERO_COLLECTION_NAME', ''),
        'ZOTERO_COLLECTION_KEY': config.get('ZOTERO_COLLECTION_KEY', '')
    }

    # Format CORE_TOPICS as markdown list items
    core_topics = config.get('RELEVANCE_CRITERIA', {}).get('CORE_TOPICS', [])
    replacements['CORE_TOPICS'] = '\n'.join([f"   - {topic}" for topic in core_topics])

    # Format TRUSTWORTHY_SOURCES as markdown list items for AGENTS.md
    sources = config.get('TRUSTWORTHY_SOURCES', [])
    replacements['TRUSTWORTHY_SOURCES'] = '\n'.join([
        f"   - **{s.get('name')}** (`{s.get('domain')}`) — {s.get('description')}" for s in sources
    ])

    # Format TRUSTWORTHY_SOURCES as numbered list items for SKILL.md
    replacements['TRUSTWORTHY_SOURCES_LIST'] = '\n'.join([
        f"{i}. **{s.get('name')}** (`{s.get('domain')}`) – {s.get('description')}" for i, s in enumerate(sources, 1)
    ])

    # Format EXAMPLE_SEARCH_QUERIES as markdown list items for SKILL.md
    queries = config.get('EXAMPLE_SEARCH_QUERIES', [])
    replacements['EXAMPLE_SEARCH_QUERIES_LIST'] = '\n'.join([
        f"- `{query}`" for query in queries
    ])

    # Evaluation Guidelines
    guidelines = config.get('RELEVANCE_CRITERIA', {}).get('EVALUATION_GUIDELINES', {})
    replacements['HIGH_PRIORITY_DIRECT'] = guidelines.get('HIGH_PRIORITY_DIRECT', '')
    replacements['MEDIUM_PRIORITY_TRANSFERABLE'] = guidelines.get('MEDIUM_PRIORITY_TRANSFERABLE', '')
    replacements['LOW_PRIORITY_SKIP'] = guidelines.get('LOW_PRIORITY_SKIP', '')

    # 2. Process templates
    templates = [
        ('.agents/AGENTS.md.template', '.agents/AGENTS.md'),
        ('.agents/skills/web-news-expander/SKILL.md.template', '.agents/skills/web-news-expander/SKILL.md')
    ]

    for template_path, target_path in templates:
        if not os.path.exists(template_path):
            print(f"Error: Template {template_path} not found.")
            continue
        
        print(f"Processing template {template_path} -> {target_path}...")
        with open(template_path, 'r') as f:
            content = f.read()
        
        for placeholder, value in replacements.items():
            content = content.replace(f"{{{{{placeholder}}}}}", str(value))
            
        with open(target_path, 'w') as f:
            f.write(content)

    print("Agent system successfully initialized!")

if __name__ == '__main__':
    main()
