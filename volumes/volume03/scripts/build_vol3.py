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
chapters_dir = os.path.join(volumes_dir, "volume03", "chapters")
diagrams_dir = os.path.join(volumes_dir, "volume03", "diagrams")

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
            slug = re.sub(r'[^a-zA-Z0-9]+', '-', clean_title).strip('-').lower()
            if slug:
                header_text = slug
                
        mermaid_code = match.group(1).strip()
        mermaid_code = html.unescape(mermaid_code)
        
        mermaid_code = mermaid_code.replace('C[("Time-Series <br/> Database (TSDB)")] <-- "Scrapes Port 9100 <br/> every 15s" --- B', 'B -->|"Scrapes Port 9100 <br/> every 15s"| C[("Time-Series <br/> Database (TSDB)")]')
        mermaid_code = mermaid_code.replace('A -.->|"Threshold: >100 Lines"| D', 'A -. "Threshold: >100 Lines" .-> D')
        mermaid_code = mermaid_code.replace('<-->|"Collaborates on CI/CD"|', '<-->')
        mermaid_code = mermaid_code.replace('\\n', '<br/>')
        
        mermaid_code = '%%{init: {"theme": "default", "fontFamily": "Arial, sans-serif"}}%%\n' + mermaid_code
        
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
        return f'src="{os.path.join(volumes_dir, "volume03", src)}"'
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
    /* Margins and Page numbers are now handled natively by Playwright via display_header_footer */

    body { font-family: 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.5; font-size: 13pt; color: #333; }
    
    h1.volume-title { color: #2c3e50; font-size: 36pt; text-align: center; margin-top: 40%; page-break-before: always; }
    h2.chapter-h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-top: 24pt; margin-bottom: 12pt; page-break-before: always; font-size: 20pt; }
    
    h2 { color: #2980b9; margin-top: 18pt; margin-bottom: 8pt; font-size: 16pt; }
    h3 { color: #34495e; margin-top: 14pt; margin-bottom: 6pt; }
    
    code { background-color: #f1f2f6; padding: 2px 4px; font-family: 'Consolas', Courier, monospace; font-size: 9.5pt; color: #e74c3c; border-radius: 3px; }
    
    /* Terminal Style Code Blocks */
    pre { 
        background-color: #1e1e1e; 
        color: #d4d4d4; 
        padding: 12pt 12pt 12pt 12pt; 
        font-family: 'Consolas', Courier, monospace; 
        font-size: 10pt; 
        border-radius: 6px; 
        white-space: pre-wrap; 
        word-wrap: break-word; 
        page-break-inside: avoid;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #333;
    }
    /* macOS style dots */
    pre::before {
        content: "•••";
        color: transparent;
        display: block;
        margin-bottom: 10px;
        font-size: 0;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #ff5f56;
        box-shadow: 20px 0 0 #ffbd2e, 40px 0 0 #27c93f;
    }
    
    pre code { color: inherit; background-color: transparent; padding: 0; }
    
    hr { margin: 15pt 0; border: none; border-top: 1px solid #bdc3c7; }
    blockquote { border-left: 4px solid #bdc3c7; margin: 10pt 0; padding-left: 12pt; color: #57606f; font-style: italic; background-color: #f8f9fa; padding: 10pt; border-radius: 0 5px 5px 0; page-break-inside: avoid; }
    table { border-collapse: collapse; width: 100%; margin-top: 10pt; margin-bottom: 15pt; font-size: 10pt; page-break-inside: auto; }
    tr { page-break-inside: avoid; page-break-after: auto; }
    
    ul, ol { margin-top: 6pt; margin-bottom: 10pt; padding-left: 25pt; }
    li { margin-top: 3pt; margin-bottom: 3pt; line-height: 1.4; }
    p { margin-top: 0; margin-bottom: 10pt; line-height: 1.5; }
    
    th, td { border: 1px solid #dfe4ea; padding: 8pt; text-align: left; }
    th { background-color: #f1f2f6; color: #2f3542; font-weight: bold; }
    a { color: #0000EE; text-decoration: none; }
    
    .mermaid-diagram { text-align: center; margin: 15pt 0; page-break-inside: avoid; }
    .mermaid-diagram img { max-width: 100%; max-height: 500px; }
    
    .chapter-anchor { display: block; height: 0; overflow: hidden; }

    /* Custom Admonitions / Callouts */
    .metadata-box {
        background-color: #f1f4f9;
        border: 1px solid #d2dce8;
        border-radius: 8px;
        padding: 15pt;
        margin: 15pt 0;
        font-size: 10.5pt;
        page-break-inside: avoid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metadata-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8pt 20pt;
    }
    .metadata-item {
        display: flex;
        flex-direction: column;
    }
    .metadata-key {
        font-weight: bold;
        color: #5f6368;
        text-transform: uppercase;
        font-size: 8.5pt;
        letter-spacing: 0.5px;
    }
    .metadata-value {
        color: #202124;
    }
    
    .callout {
        margin: 15pt 0;
        padding: 12pt 12pt 12pt 40pt;
        border-radius: 6px;
        border-left: 5px solid #ccc;
        page-break-inside: avoid;
        position: relative;
        font-style: normal;
        background-color: #f8f9fa;
        color: #2c3e50;
    }
    .callout-title {
        font-weight: bold;
        margin-bottom: 5px;
        text-transform: uppercase;
        font-size: 9pt;
        letter-spacing: 0.5px;
    }
    
    .callout-note { border-left-color: #0969da; background-color: #f0f6fc; }
    .callout-note .callout-title { color: #0969da; }
    
    .callout-tip { border-left-color: #1a7f37; background-color: #f1f8f3; }
    .callout-tip .callout-title { color: #1a7f37; }
    
    .callout-important { border-left-color: #8250df; background-color: #f7f2fb; }
    .callout-important .callout-title { color: #8250df; }
    
    .callout-warning { border-left-color: #9a6700; background-color: #fff8c5; }
    .callout-warning .callout-title { color: #9a6700; }
    
    .callout-caution { border-left-color: #d1242f; background-color: #ffebe9; }
    .callout-caution .callout-title { color: #d1242f; }
</style>
"""

all_html = f"<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n{css}\n</head>\n<body>\n"

volumes = ["volume03"]

toc_html = "<div class='toc-page'><h1 class='volume-title' style='margin-top: 10%;'>Table of Contents</h1><ul style='list-style: none; padding: 0; font-size: 14pt; line-height: 2;'>\n"

for vol in volumes:
    vol_num = vol.split('-')[1].lstrip('0') if '-' in vol else vol.replace('volume', '').lstrip('0')
    vol_title = vol.replace('-', ' ').title()
    
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
        anchor = f'<a id="{chap_basename}" class="chapter-anchor"></a>\n'
        
        # Insert metadata HTML just after the chapter title (which is now h2.chapter-h2)
        if metadata_html:
            html_out = re.sub(r'(<h2 class="chapter-h2".*?</h2>)', r'\1\n' + metadata_html, html_out, count=1)
            
        all_html += anchor + html_out + "\n"
        
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
            
            panchor = f'<a name="{practice_name}" class="chapter-anchor"></a>\n'
            all_html += panchor + phtml + "\n"

# Replace image paths
all_html = re.sub(r'src="([^"]+)"', fix_img_src, all_html)

# Convert internal links
all_html = re.sub(r'href="([^"]+)"', fix_links, all_html)

# Process Admonitions
all_html = process_admonitions(all_html)

# Process Mermaid diagrams
all_html = process_mermaid_blocks(all_html)

toc_html += "</ul></div>\n"
all_html = all_html.replace('<!-- TOC -->', f'<a name="TOC.md"></a>\n{toc_html}')

all_html += "\n</body>\n</html>"

html_file = os.path.join(build_dir, "book_full.html")
print("Saving HTML...")
with open(html_file, "w", encoding="utf-8") as f:
    f.write(all_html)

# Create Cover HTML
cover_pdf_path = os.path.join(build_dir, 'Cover.pdf')
if not os.path.exists(cover_pdf_path):
    cover_pdf_path = os.path.join(build_dir, 'cover.pdf')

cover_img = "cover.png"
if os.path.exists(cover_pdf_path):
    import fitz
    doc = fitz.open(cover_pdf_path)
    page = doc[0]
    pix = page.get_pixmap(dpi=150)
    pix.save(os.path.join(build_dir, "cover.png"))

cover_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; background: #fff; }}
img {{ width: 100%; height: 100%; object-fit: contain; }}
</style>
</head>
<body>
<img src="{cover_img}" />
</body>
</html>
"""
cover_html_file = os.path.join(build_dir, "cover.html")
with open(cover_html_file, "w", encoding="utf-8") as f:
    f.write(cover_html)

print("Generating PDF with Playwright...")
final_pdf = os.path.join(repo_root, "handbooks", "Linux_Support_Engineer_Master_Handbook_Vol3.pdf")

try:
    from playwright.sync_api import sync_playwright
    
    temp_pdf = os.path.join(build_dir, "book_temp_playwright.pdf")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{html_file.replace(chr(92), '/')}", wait_until="networkidle")
        
        import datetime
        build_uuid = str(uuid.uuid4())
        build_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        purchase_id = "RC1-PREVIEW"
        manifest = f"Licensed Copy | Purchase ID: {purchase_id} | Build: {build_uuid}"

        header_template = '<div style="font-size: 9px; font-family: Segoe UI, sans-serif; letter-spacing: 0.5px; width: 100%; text-align: center;"></div>'
        footer_template = f'<div style="font-size: 8px; font-family: Segoe UI, sans-serif; letter-spacing: 0.5px; width: 100%; display: flex; justify-content: space-between; margin: 0 20mm;"><span style="color: #000;">Linux Support Engineer Master Handbook</span><span style="color: #aaa; font-size: 6px;">{manifest}</span><span style="color: #000;">Page <span class="pageNumber"></span></span></div>'
        
        page.pdf(
            path=temp_pdf,
            format="Letter",
            margin={"top": "10mm", "bottom": "15mm", "left": "20mm", "right": "20mm"},
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            print_background=True
        )
        browser.close()
    
    # Prepend cover using PyMuPDF if it exists
    cover_pdf_path = os.path.join(build_dir, 'Cover.pdf')
    if not os.path.exists(cover_pdf_path):
        cover_pdf_path = os.path.join(build_dir, 'cover.pdf')

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
        doc.save(final_pdf)
        doc.close()
        cover_doc.close()
        os.remove(temp_pdf)
    else:
        os.rename(temp_pdf, final_pdf)
        
    print(f"Generated {final_pdf} successfully!")

except Exception as e:
    print(f"Failed to generate PDF with Playwright: {e}")

print("Cleaned up root build directory.")
