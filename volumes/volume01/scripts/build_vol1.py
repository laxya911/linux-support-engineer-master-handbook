import os
import re
import markdown
import uuid
import html
import hashlib
import textwrap
import subprocess
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
build_dir = os.path.join(repo_root, "build")
volumes_dir = os.path.join(repo_root, "volumes")
chapters_dir = os.path.join(volumes_dir, "volume01", "chapters")
diagrams_dir = os.path.join(volumes_dir, "volume01", "diagrams")

if not os.path.exists(diagrams_dir):
    os.makedirs(diagrams_dir)

def process_admonitions(html_text):
    def bq_replacer(match):
        bq_content = match.group(1)
        if not re.search(r'\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', bq_content, re.IGNORECASE):
            return match.group(0)
            
        parts = re.split(r'<p>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', bq_content, flags=re.IGNORECASE)
        
        if len(parts) == 1:
             return match.group(0)
             
        out = parts[0]
        for i in range(1, len(parts), 2):
            admon_type = parts[i].lower()
            raw_content = parts[i+1].strip()
            
            title_match = re.match(r'(.*?)(?:\n|<br\s*/?>)(.*)', raw_content, flags=re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                content = title_match.group(2).strip()
            else:
                title = ''
                content = raw_content
                
            display_title = title if title else admon_type.upper()
            out += f'<div class="callout callout-{admon_type}"><div class="callout-title">{display_title}</div><p>{content}</div>'
            
        return out

    pattern = r'<blockquote>(.*?)</blockquote>'
    html_text = re.sub(pattern, bq_replacer, html_text, flags=re.DOTALL | re.IGNORECASE)
    return html_text


def process_terminals(html_text):
    pattern = re.compile(r'<pre[^>]*><code class="language-(bash|shell|terminal)">\s*(.*?)\s*</code></pre>', flags=re.DOTALL)
    def replacer(match):
        lang = match.group(1)
        code_content = match.group(2)
        return f'''<div class="terminal-window">
<div class="terminal-header">
    <div class="terminal-dots">
        <div class="terminal-dot dot-red"></div>
        <div class="terminal-dot dot-yellow"></div>
        <div class="terminal-dot dot-green"></div>
    </div>
    <div class="terminal-title">{lang}</div>
</div>
<div class="terminal-content"><pre><code>{code_content}</code></pre></div>
</div>'''
    return re.sub(pattern, replacer, html_text)

def process_navigation(html_text):
    pattern = re.compile(r'(<h2[^>]*>Navigation</h2>.*?)(?=</div>|$)', flags=re.DOTALL)
    def replacer(match):
        nav_content = match.group(1)
        return f'<div class="nav-block">{nav_content}</div>'
    return re.sub(pattern, replacer, html_text)

def process_mermaid_blocks(html_text):
    import requests
    import re
    import hashlib
    import html
    
    pattern = re.compile(r'<pre[^>]*><code class="language-mermaid">\s*(.*?)\s*</code></pre>', flags=re.DOTALL)
    out_html = ""
    last_end = 0
    
    for match in pattern.finditer(html_text):
        out_html += html_text[last_end:match.start()]
        
        header_text = "diagram"
        preceding = html_text[:match.start()]
        h_match = list(re.finditer(r'<h[1-6][^>]*>(.*?)</h[1-6]>', preceding))
        if h_match:
            raw_title = h_match[-1].group(1)
            clean_title = re.sub(r'<[^>]+>', '', raw_title).strip()
            clean_title = re.sub(r'(?i)^Visual Architecture:?\s*', '', clean_title).strip()
            slug = re.sub(r'[^a-zA-Z0-9]+', '-', clean_title).strip('-').lower()
            if slug:
                header_text = slug
                
        mermaid_code = match.group(1).strip()
        mermaid_code = html.unescape(mermaid_code)
        
        mermaid_code = mermaid_code.replace('C[("Time-Series <br/> Database (TSDB)")] <-- "Scrapes Port 9100 <br/> every 15s" --- B', 'B -->|"Scrapes Port 9100 <br/> every 15s"| C[("Time-Series <br/> Database (TSDB)")]')
        mermaid_code = mermaid_code.replace('A -.->|"Threshold: >100 Lines"| D', 'A -. "Threshold: >100 Lines" .-> D')
        mermaid_code = mermaid_code.replace('<-->|"Collaborates on CI/CD"|', '<-->')
        mermaid_code = mermaid_code.replace('\\n', '<br/>')
        
        mermaid_code = '%%{init: {"theme": "default", "fontFamily": "Arial, sans-serif", "flowchart": {"htmlLabels": false}}}%%\n' + mermaid_code
        
        img_name = f"{header_text}.svg"
        img_path = os.path.join(diagrams_dir, img_name)
        
        if os.path.exists(img_path):
            out_html += f'<div class="mermaid-diagram"><img src="{img_path}" /></div>'
        else:
            print(f"Fetching diagram {img_name}...")
            try:
                r = requests.post('https://kroki.io', json={'diagram_source': mermaid_code, 'diagram_type': 'mermaid', 'output_format': 'svg'}, timeout=15)
                if r.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(r.content)
                    out_html += f'<div class="mermaid-diagram"><img src="{img_path}" /></div>'
                else:
                    print(f"kroki failed, status {r.status_code}")
                    out_html += f"<pre><code>{mermaid_code}</code></pre>"
            except Exception as e:
                print(f"kroki request failed: {e}")
                out_html += f"<pre><code>{mermaid_code}</code></pre>"
                
        last_end = match.end()
        
    out_html += html_text[last_end:]
    return out_html

def fix_img_src(match):
    src = match.group(1)
    if src.startswith('../assets/'):
        return f'src="{os.path.join(volumes_dir, "volume01", src)}"'
    elif src.startswith('../../assets/'):
        return f'src="{os.path.join(repo_root, src[6:])}"'
    return match.group(0)

def fix_links(match):
    href = match.group(1)
    if href.endswith('.md'):
        if href.startswith('#'):
            return match.group(0)
        # Convert to internal anchor
        anchor = href.split('/')[-1]
        return f'href="#{anchor}"'
    return match.group(0)

volumes = []
for d in sorted(os.listdir(volumes_dir)):
    if d.startswith("volume-") and os.path.isdir(os.path.join(volumes_dir, d)):
        volumes.append(d)

css = """
    <style>
    body { font-family: 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.6; font-size: 13pt; color: #202124; margin: 0; padding: 0; }
    
    h1.volume-title { color: #2c3e50; font-size: 38pt; text-align: center; margin-top: 40%; page-break-after: avoid; font-weight: 800; letter-spacing: -1px; }
    h2.chapter-h2 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 8px; margin-top: 30pt; margin-bottom: 16pt; page-break-before: always; font-size: 24pt; font-weight: 700; }
    
    h2 { color: #2980b9; margin-top: 24pt; margin-bottom: 12pt; font-size: 18pt; font-weight: 600; }
    h3 { color: #34495e; margin-top: 20pt; margin-bottom: 10pt; font-size: 15pt; font-weight: 600; }
    p { margin-bottom: 14pt; }
    
    a { color: #2980b9; text-decoration: none; }
    
    code { font-family: 'Consolas', 'Courier New', monospace; background-color: #f1f3f4; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; color: #d63031; }
    pre { background-color: #f8f9fa; border-left: 4px solid #bdc3c7; padding: 12pt; overflow-x: auto; font-size: 11pt; border-radius: 0 4px 4px 0; box-shadow: inset 0 0 10px rgba(0,0,0,0.02); }
    pre code { background-color: transparent; padding: 0; color: #2d3436; font-size: 1em; }
    
    table { width: 100%; border-collapse: collapse; margin-bottom: 16pt; font-size: 11pt; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    th, td { border: 1px solid #e0e0e0; padding: 10pt; text-align: left; }
    th { background-color: #f8f9fa; font-weight: bold; color: #202124; }
    
    .mermaid-diagram { text-align: center; margin: 20pt 0; }
    .mermaid-diagram img { max-width: 100%; height: auto; }
    
    blockquote { border-left: 4px solid #dfe1e5; margin: 16pt 0; padding-left: 16pt; color: #5f6368; font-style: italic; background: transparent; }
    
    .callout {
        margin: 10pt 0;
        padding: 10pt 16pt 10pt 48pt;
        border-radius: 8px;
        border-left: 6px solid #ccc;
        position: relative;
        font-style: normal;
        background-color: #f8f9fa;
        color: #202124;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        page-break-inside: avoid;
        break-inside: avoid;
    }
    .callout p { line-height: 1.4; margin: 2pt 0; }
    .callout-title { margin-bottom: 4pt; }
    
    .callout::before {
        content: "";
        position: absolute;
        left: 16pt;
        top: 16pt;
        width: 20pt;
        height: 20pt;
        background-repeat: no-repeat;
        background-size: contain;
    }
    
    .callout-title {
        font-weight: bold;
        margin-bottom: 8pt;
        font-size: 11pt;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Info/Note */
    .callout-note { border-left-color: #0969da; background-color: #f0f6fc; }
    .callout-note .callout-title { color: #0969da; }
    .callout-note::before { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230969da' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'%3E%3C/circle%3E%3Cline x1='12' y1='16' x2='12' y2='12'%3E%3C/line%3E%3Cline x1='12' y1='8' x2='12.01' y2='8'%3E%3C/line%3E%3C/svg%3E"); }
    
    /* Tip/Success */
    .callout-tip { border-left-color: #1a7f37; background-color: #f1f8f3; }
    .callout-tip .callout-title { color: #1a7f37; }
    .callout-tip::before { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231a7f37' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M22 11.08V12a10 10 0 1 1-5.93-9.14'%3E%3C/path%3E%3Cpolyline points='22 4 12 14.01 9 11.01'%3E%3C/polyline%3E%3C/svg%3E"); }
    
    /* Important/Incident */
    .callout-important { border-left-color: #8250df; background-color: #f7f2fb; }
    .callout-important .callout-title { color: #8250df; }
    .callout-important::before { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%238250df' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolygon points='13 2 3 14 12 14 11 22 21 10 12 10 13 2'%3E%3C/polygon%3E%3C/svg%3E"); }
    
    /* Warning */
    .callout-warning { border-left-color: #9a6700; background-color: #fff8c5; }
    .callout-warning .callout-title { color: #9a6700; }
    .callout-warning::before { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%239a6700' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'%3E%3C/path%3E%3Cline x1='12' y1='9' x2='12' y2='13'%3E%3C/line%3E%3Cline x1='12' y1='17' x2='12.01' y2='17'%3E%3C/line%3E%3C/svg%3E"); }
    
    /* Caution/Danger */
    .callout-caution { border-left-color: #d1242f; background-color: #ffebe9; }
    .callout-caution .callout-title { color: #d1242f; }
    .callout-caution::before { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23d1242f' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolygon points='7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2'%3E%3C/polygon%3E%3Cline x1='15' y1='9' x2='9' y2='15'%3E%3C/line%3E%3Cline x1='9' y1='9' x2='15' y2='15'%3E%3C/line%3E%3C/svg%3E"); }
    
    .toc-page { page-break-before: always; }
    .nav-block {
        margin-top: 30pt;
        padding-top: 10pt;
        border-top: 1px solid #e2e8f0;
    }
    .nav-block p {
        margin: 2pt 0;
        line-height: 1.2;
        font-size: 10pt;
        color: #475569;
    }
    .nav-block a {
        display: inline-block;
        margin-bottom: 6pt;
    }
    .metadata-box { background-color: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin-bottom: 25px; border-left: 5px solid #2980b9; }
    .metadata-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .metadata-item { font-size: 11pt; line-height: 1.4; display: flex; align-items: baseline; }
    .metadata-key { font-weight: 600; color: #5f6368; width: 140px; flex-shrink: 0; }
    /* Block Splitting Prevention */
    img { break-inside: avoid; display: block; margin: 20px auto; max-width: 100%; height: auto; }
    .mermaid { break-inside: avoid; text-align: center; margin: 20px 0; }
    table { break-inside: avoid; width: 100%; border-collapse: collapse; margin-bottom: 16pt; font-size: 11pt; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .callout { page-break-inside: avoid; break-inside: avoid; }
    
    /* Terminal Block CSS */
    .terminal-window {
        background-color: #2b2b2b;
        border-radius: 6px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin: 20px 0;
        overflow: hidden;
        font-family: 'Consolas', 'Courier New', monospace;
        break-inside: avoid;
    }
    .terminal-header {
        background-color: #3c3f41;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #2b2b2b;
    }
    .terminal-dots { display: flex; gap: 6px; margin-left: 4px; }
    .terminal-dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-red { background-color: #ff5f56; }
    .dot-yellow { background-color: #ffbd2e; }
    .dot-green { background-color: #27c93f; }
    .terminal-title {
        color: #a9b7c6;
        font-size: 9pt;
        text-align: center;
        flex-grow: 1;
        margin-right: 36px;
    }
    .terminal-content {
        padding: 15px;
        color: #a9b7c6;
        font-size: 9.5pt;
        line-height: 1.4;
        background-color: #2b2b2b;
    }
    .terminal-content pre, .terminal-content code {
        background-color: transparent !important;
        color: #a9b7c6 !important;
        margin: 0;
        padding: 0;
        border: none !important;
        white-space: pre-wrap;
        box-shadow: none;
    }

</style>
"""

all_html = f"<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n{css}\n</head>\n<body>\n"



volumes = ["volume01"]

toc_html = "<div class='toc-page'><h1 class='volume-title' style='margin-top: 10%;'>Table of Contents</h1><ul style='list-style: none; padding: 0; font-size: 14pt; line-height: 2;'>\n"

for vol in volumes:
    vol_num = vol.replace('volume', '').lstrip('0')
    vol_title = f"Volume {vol_num}"
    
    # Add volume to TOC
    toc_html += f"<li style='font-weight: bold; margin-top: 15pt;'>Volume {vol_num}</li>\n"
    
    chapters_dir = os.path.join(volumes_dir, vol, "chapters")
    practice_dir = os.path.join(volumes_dir, vol, "practice-files")
    
    chapters = []
    for f in sorted(os.listdir(chapters_dir)):
        if f.endswith('.md') and not f.startswith('CHAPTER_TEMPLATE'):
            chapters.append(os.path.join(chapters_dir, f))
            
    for chap in chapters:
        with open(chap, 'r', encoding='utf-8') as f:
            md_text = f.read()
            
        # Extract title for TOC
        title_match = re.search(r'^#\s+(.*?)$', md_text, re.MULTILINE)
        chap_title = title_match.group(1) if title_match else os.path.basename(chap)
        
        chap_basename = os.path.basename(chap)
        toc_html += f"<li><a style='color: #2980b9; text-decoration: none;' href='#{chap_basename}'>{chap_title}</a></li>\n"
            
        # Parse YAML frontmatter
        metadata_html = ""
        yaml_match = re.search(r'^---(.*?)---\n', md_text, flags=re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1).strip()
            md_text = md_text[yaml_match.end():]
            
            # Build two-column grid
            items = []
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip().replace('_', ' ').title()
                    val = val.strip()
                    if key.lower() not in ['title', 'chapter', 'volume', 'part', 'id', 'author', 'reviewed by', 'learning outcomes']:
                        if key.lower() == 'prerequisites' and re.match(r'^V\d-C\d+$', val):
                            # Try to find the matching chapter file for the anchor
                            matched_chap = next((os.path.basename(c) for c in chapters if val in c), None)
                            if matched_chap:
                                val = f'<a href="#{matched_chap}">{val}</a>'
                        items.append(f'<div class="metadata-item"><span class="metadata-key">{key}</span><span class="metadata-value">{val}</span></div>')
            
            if items:
                metadata_html = '<div class="metadata-box"><div class="metadata-grid">\n' + '\n'.join(items) + '\n</div></div>\n'
        
        md_text = md_text.replace('⬅', '&larr;')
        md_text = md_text.replace('➡', '&rarr;')
        md_text = md_text.replace('🏠', '&uarr;')
        
        # Parse markdown
        html_out = markdown.markdown(md_text, extensions=['pymdownx.superfences', 'tables'])
        
        # Demote heading levels: h3->h4, h2->h3, h1->h2
        html_out = html_out.replace('<h3', '<h4').replace('</h3', '</h4')
        html_out = html_out.replace('<h2', '<h3').replace('</h2', '</h3')
        html_out = html_out.replace('<h1', '<h2 class="chapter-h2"').replace('</h1', '</h2')
        
        # Add anchor and metadata
        chap_basename = os.path.basename(chap)
        # anchor removed to avoid blank pages
        
        # Insert metadata HTML just after the chapter title (which is now h2.chapter-h2)
        if metadata_html:
            html_out = re.sub(r'(<h2 class="chapter-h2".*?</h2>)', r'\1\n' + metadata_html, html_out, count=1)
            
        html_out = re.sub(r'<h2 class="chapter-h2"', f'<h2 id="{chap_basename}" class="chapter-h2"', html_out, count=1)
        all_html += html_out + "\n"
        
        # Handle practice file
        practice_file = chap_basename.replace('.md', '').split('-')
        practice_name = f"{practice_file[0]}-{practice_file[1]}-practice.md"
        practice_path = os.path.join(practice_dir, practice_name)
        if os.path.exists(practice_path):
            with open(practice_path, 'r', encoding='utf-8') as pf:
                pmd_text = pf.read()
            pmd_text = re.sub(r'^---.*?---\n', '', pmd_text, flags=re.DOTALL)
            pmd_text = pmd_text.replace('⬅', '&larr;')
            pmd_text = pmd_text.replace('➡', '&rarr;')
            pmd_text = pmd_text.replace('🏠', '&uarr;')
            phtml = markdown.markdown(pmd_text, extensions=['pymdownx.superfences', 'tables'])
            
            phtml = phtml.replace('<h3', '<h4').replace('</h3', '</h4')
            phtml = phtml.replace('<h2', '<h3').replace('</h2', '</h3')
            phtml = phtml.replace('<h1', '<h2 class="chapter-h2"').replace('</h1', '</h2')
            
            phtml = re.sub(r'<h2 class="chapter-h2"', f'<h2 id="{practice_name}" class="chapter-h2"', phtml, count=1)
            all_html += phtml + "\n"

# Replace image paths
all_html = re.sub(r'src="([^"]+)"', fix_img_src, all_html)

# Convert internal links
all_html = re.sub(r'href="([^"]+)"', fix_links, all_html)

# Process Admonitions
all_html = process_admonitions(all_html)

# Process Mermaid diagrams
all_html = process_terminals(all_html)
all_html = process_navigation(all_html)
all_html = process_mermaid_blocks(all_html)
all_html = all_html.replace('<h3>Hands-on Lab</h3>', '<h3 style="page-break-before: always; margin-top: 30pt;">Hands-on Lab</h3>')

toc_html += "</ul></div>\n"
all_html = all_html.replace('<!-- TOC -->', f'<a name="TOC.md"></a>\n{toc_html}')

all_html += "\n</body>\n</html>"

html_file = os.path.join(build_dir, "book_full.html")
print("Saving HTML...")
with open(html_file, "w", encoding="utf-8") as f:
    f.write(all_html)

# Volume 1 Specific Cover
import shutil
source_cover_pdf = os.path.join(repo_root, "assets", "covers", "book cover volume-01.pdf")
cover_pdf_path = os.path.join(build_dir, "Cover_Vol1.pdf")
if os.path.exists(source_cover_pdf):
    shutil.copy(source_cover_pdf, cover_pdf_path)
else:
    cover_pdf_path = os.path.join(build_dir, 'Cover.pdf')


print("Generating PDF with Playwright...")
final_pdf = os.path.join(repo_root, "handbooks", "Linux_Support_Engineer_Master_Handbook_Vol1.pdf")

try:
    from playwright.sync_api import sync_playwright
    
    temp_pdf = os.path.join(build_dir, "book_temp_playwright.pdf")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(); page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        page.goto(f"file:///{html_file.replace(chr(92), '/')}", wait_until="networkidle")
        
        # Generate Book Manifest Data
        import uuid
        import datetime
        import json
        
        build_uuid = str(uuid.uuid4())
        build_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        purchase_id = "RC1-PREVIEW"
        
        manifest = f"Licensed Copy | Purchase ID: {purchase_id} | Build: {build_uuid}"
        
        header_template = '<div style="font-size: 9px; font-family: Segoe UI, sans-serif; letter-spacing: 0.5px; width: 100%; text-align: center;"></div>'
        footer_template = f'<div style="font-size: 8px; font-family: Segoe UI, sans-serif; letter-spacing: 0.5px; width: 100%; display: flex; justify-content: space-between; margin: 0 20mm;"><span style="color: #000;">Linux Support Engineer Master Handbook</span><span style="color: #aaa; font-size: 6px;">{manifest}</span><span style="color: #000;">Page <span class="pageNumber"></span></span></div>'
        
        page.pdf(
            path=temp_pdf,
            width="8.2307in",
            height="11.3077in",
            margin={"top": "10mm", "bottom": "15mm", "left": "20mm", "right": "20mm"},
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            print_background=True
        )
        browser.close()
    
    # Prepend cover using PyMuPDF if it exists
    cover_pdf_path = os.path.join(build_dir, 'Cover_Vol1.pdf')
    if not os.path.exists(cover_pdf_path):
        cover_pdf_path = os.path.join(build_dir, 'Cover.pdf')

    if os.path.exists(cover_pdf_path):
        print("Prepending cover...")
        import fitz
        doc = fitz.open(temp_pdf)
        cover_doc = fitz.open(cover_pdf_path)
        doc.insert_pdf(cover_doc, from_page=0, to_page=0, start_at=0)
        # Update links since we shifted pages by 1
        for pdf_page in doc:
            for link in pdf_page.links():
                if link["kind"] == fitz.LINK_GOTO:
                    link["page"] += 1
                    pdf_page.update_link(link)
        
        # Inject comprehensive metadata
        meta = {
            "title": "Linux Support Engineer Master Handbook - Volume 1: Linux Fundamentals",
            "author": "Laxman Aryal",
            "subject": "Linux Administration and Support Engineering",
            "keywords": f"Linux, System Administration, Support Engineer, RC1, Build-{build_uuid}",
            "creator": "Aryal Technical Press",
            "producer": "Aryal Technical Press Build Pipeline"
        }
        doc.set_metadata(meta)
        
        doc.save(final_pdf)
        doc.close()
        cover_doc.close()
        os.remove(temp_pdf)
    else:
        os.rename(temp_pdf, final_pdf)
        
    print(f"Generated {final_pdf} successfully!")

except Exception as e:
    print(f"Failed to generate PDF with Playwright: {e}")


