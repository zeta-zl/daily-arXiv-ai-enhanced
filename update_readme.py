import os
from os.path import join

import re
from collections import defaultdict

def fold_links_by_year_month(content):

    # 提取所有形如 [YYYY-MM-DD](data/YYYY-MM-DD.md) 的链接
    pattern = r'\[(\d{4})-(\d{2})-(\d{2})\]\(data[\\/]\1-\2-\3\.md\)'
    matches = re.findall(pattern, content)

    grouped = defaultdict(lambda: defaultdict(list))
    today_line = None
    for y, m, d in matches:
        date_str = f"{y}-{m}-{d}"
        md_link = f"[{date_str}](data/{date_str}.md)"
        grouped[y][m].append(md_link)
        if not today_line:
            today_line = md_link

    folded_md = f"# Content\n\n{today_line}\n\n"
    for y in sorted(grouped.keys(), reverse=True):
        folded_md += f"<details>\n<summary>{y}</summary>\n\n"
        for m in sorted(grouped[y].keys(), reverse=True):
            folded_md += f"<details>\n<summary>&emsp;{y}-{m}</summary>\n\n"
            for link in sorted(grouped[y][m], reverse=True):
                folded_md += f"{link}\n\n"
            folded_md += "</details>\n\n"
        folded_md += "</details>\n\n"

    new_content = re.sub(
        r'# Content.*?# Related tools',
        folded_md + '# Related tools',
        content,
        flags=re.DOTALL
    )

    return new_content


if __name__ == '__main__':
    template = open('template.md', 'r').read()
    data = sorted(os.listdir('data'), reverse=True)

    readme_content_template = open('readme_content_template.md', 'r').read()
    readme_content = "\n\n".join(
        [readme_content_template.format(date=item.replace('.md', ''),url=join('data', item)) for item in data if item.endswith('.md')]
    )
    markdown = template.format(readme_content=readme_content)
    new_content = fold_links_by_year_month(markdown)
    with open('README.md', 'w') as f:
        f.write(new_content)
    # fold_links_by_year_month('README.md')