#!/usr/bin/env python3
import os
import markdown2
from weasyprint import HTML, CSS
from pathlib import Path
from bs4 import BeautifulSoup
import re

def sanitize_anchor(text):
    """Create valid HTML anchor from text"""
    return re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '-').lower()

def create_pdf_from_repo(repo_path, output_name):
    repo_path = Path(repo_path)

    # Debug: Show what we're looking for
    print(f"Searching in: {repo_path.absolute()}")
    print(f"Directory exists: {repo_path.exists()}")

    if not repo_path.exists():
        print(f"❌ Directory {repo_path} does not exist!")
        return

    # Find ALL markdown files recursively, including in subdirectories
    md_files = []
    for md_file in repo_path.rglob("*.md"):
        if md_file.is_file():
            md_files.append(md_file)

    # Sort files by path for logical ordering
    md_files = sorted(md_files)

    print(f"Found {len(md_files)} markdown files:")
    for f in md_files[:10]:  # Show first 10 files
        print(f"  - {f.relative_to(repo_path)}")
    if len(md_files) > 10:
        print(f"  ... and {len(md_files) - 10} more files")

    if not md_files:
        print(f"❌ No markdown files found in {repo_path}")
        # Debug: Show what files ARE in the directory
        print("Files in directory:")
        for item in repo_path.rglob("*"):
            if item.is_file():
                print(f"  - {item.relative_to(repo_path)}")
        return

    # CSS for better formatting
    css_content = """
    @page {
        margin: 2cm;
        @bottom-center {
            content: counter(page);
        }
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        line-height: 1.6;
        color: #333;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        page-break-after: avoid;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    h1 {
        font-size: 28px;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        page-break-before: always;
    }
    h2 {
        font-size: 22px;
        border-bottom: 1px solid #bdc3c7;
        padding-bottom: 5px;
        margin-top: 2em;
    }
    h3 { font-size: 18px; color: #34495e; }
    h4 { font-size: 16px; color: #34495e; }

    code {
        background: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.9em;
    }
    pre {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #3498db;
        overflow-x: auto;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.85em;
    }
    pre code {
        background: none;
        padding: 0;
    }

    .toc {
        page-break-after: always;
        border: 1px solid #ddd;
        padding: 20px;
        background: #f9f9f9;
    }
    .toc h2 {
        margin-top: 0;
        border-bottom: 2px solid #3498db;
    }
    .toc ul {
        list-style-type: none;
        padding-left: 0;
    }
    .toc li {
        margin: 8px 0;
        padding-left: 20px;
        border-left: 2px solid #ecf0f1;
    }
    .toc a {
        text-decoration: none;
        color: #2c3e50;
    }
    .toc a:hover {
        color: #3498db;
    }

    .file-section {
        margin-top: 40px;
        border-top: 2px solid #ecf0f1;
        padding-top: 20px;
    }
    .file-path {
        background: #3498db;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.9em;
        margin-bottom: 20px;
    }

    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    th {
        background: #f8f9fa;
        font-weight: bold;
    }

    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 20px;
        margin: 20px 0;
        font-style: italic;
        background: #f8f9fa;
        padding: 15px 20px;
    }
    """

    # Start HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{output_name} Documentation</title>
    </head>
    <body>
        <h1>{output_name} Documentation</h1>
        <p>Generated from: <code>{repo_path.absolute()}</code></p>
        <p>Total files: {len(md_files)}</p>

        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
    """

    # Generate TOC and collect content
    content_sections = []

    for i, md_file in enumerate(md_files):
        relative_path = md_file.relative_to(repo_path)
        anchor = f"section-{i}-{sanitize_anchor(str(relative_path))}"

        # Add to TOC with nested structure indication
        indent_level = len(relative_path.parts) - 1
        indent_style = f"margin-left: {indent_level * 20}px;"

        html_content += f'<li style="{indent_style}"><a href="#{anchor}">{relative_path}</a></li>\n'

        # Process markdown content
        try:
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                md_content = f.read()

            if not md_content.strip():
                print(f"⚠️  Empty file: {relative_path}")
                continue

            # Convert markdown to HTML
            html_section = markdown2.markdown(
                md_content,
                extras=[
                    'fenced-code-blocks',
                    'tables',
                    'header-ids',
                    'toc',
                    'code-friendly',
                    'cuddled-lists',
                    'metadata'
                ]
            )

            content_sections.append((anchor, relative_path, html_section))

        except Exception as e:
            print(f"❌ Error processing {md_file}: {e}")

    # Close TOC
    html_content += """
            </ul>
        </div>
    """

    # Add content sections
    for anchor, relative_path, html_section in content_sections:
        html_content += f"""
        <div class="file-section" id="{anchor}">
            <div class="file-path">{relative_path}</div>
            {html_section}
        </div>
        """

    # Close HTML
    html_content += "</body></html>"

    # Generate PDF
    try:
        print(f"Generating PDF: {output_name}.pdf")
        HTML(string=html_content).write_pdf(
            f"{output_name}.pdf",
            stylesheets=[CSS(string=css_content)]
        )

        # Check file size
        pdf_path = Path(f"{output_name}.pdf")
        if pdf_path.exists():
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            print(f"✓ Generated: {pdf_path.absolute()} ({size_mb:.1f} MB)")
        else:
            print(f"❌ PDF generation failed")

    except Exception as e:
        print(f"❌ Error generating PDF: {e}")

if __name__ == "__main__":
    # Use absolute paths to be sure
    create_pdf_from_repo("/home/anarchy1923/Projects/modelcontextprotocol/docs", "MCP-docs")

    print("\n=== Final Results ===")
    for pdf_file in Path(".").glob("*.pdf"):
        size_mb = pdf_file.stat().st_size / (1024 * 1024)
        print(f"📄 {pdf_file.absolute()} ({size_mb:.1f} MB)")
