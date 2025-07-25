# PDF Documentation Generator

Convert GitHub documentation repositories to searchable offline PDF files with table of contents.

## What This Does

Takes markdown documentation from GitHub repos and creates professional PDFs with:
- Complete table of contents
- Proper formatting and syntax highlighting
- Nested directory structure preservation
- Full-text search capability (works with `rga`, `pdfgrep`, etc.)

## Requirements

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# Install Python dependencies
pip install weasyprint markdown2 beautifulsoup4
```

## Usage

1. Clone the repos you want to convert:
```bash
git clone https://github.com/obsidianmd/obsidian-help.git
git clone https://github.com/anyproto/docs.git
```

2. Download the generator:
```bash
wget https://raw.githubusercontent.com/[your-username]/pdf-docs-generator/main/generate_pdf_docs.py
chmod +x generate_pdf_docs.py
```

3. Edit the script paths:
```python
# Change these paths to match your setup
create_pdf_from_repo("obsidian-help/en", "obsidian-help-docs")
create_pdf_from_repo("docs", "anyproto-docs")
```

4. Generate PDFs:
```bash
python3 generate_pdf_docs.py
```

## Features

- **Recursive directory scanning** - Finds all markdown files in subdirectories
- **Smart sorting** - Orders files logically by path structure
- **Professional formatting** - Clean typography with syntax highlighting
- **Error handling** - Skips problematic files and continues processing
- **Progress reporting** - Shows exactly what files are being processed
- **Size reporting** - Displays final PDF file sizes

## Output

Creates PDFs in your current directory:
- `obsidian-help-docs.pdf`
- `anyproto-docs.pdf`

Each PDF includes:
- Title page with source information
- Complete table of contents with nested structure
- All markdown content with preserved formatting
- File path headers for easy navigation

## Customization

### Change Output Directory
```python
pdf_path = Path("output") / f"{output_name}.pdf"
pdf_path.parent.mkdir(exist_ok=True)
HTML(string=html_content).write_pdf(str(pdf_path), stylesheets=[CSS(string=css_content)])
```

### Modify CSS Styling
Edit the `css_content` variable in the script to change:
- Fonts and colors
- Page margins
- Code block styling
- Table formatting

### Filter Files
Add file filtering before processing:
```python
# Skip certain files
md_files = [f for f in md_files if "draft" not in str(f)]

# Only include specific directories
md_files = [f for f in md_files if "docs" in str(f)]
```

## Integration with Search Tools

The generated PDFs work with text search tools:

```bash
# Search with ripgrep-all
rga "search term" *.pdf

# Search with pdfgrep
pdfgrep "search term" *.pdf

# Index with recoll for GUI search
recollindex -i ~/Documents/pdfs/
```

## Troubleshooting

### No markdown files found
- Check that the repository path exists
- Verify markdown files are present with `find repo_path -name "*.md"`
- Ensure you're in the correct directory

### PDF generation fails
- Install missing system dependencies: `sudo apt install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0`
- Check available disk space
- Verify write permissions in current directory

### Large file handling
For repositories with many files, the script automatically handles:
- Memory management for large documents
- Progress reporting during processing
- File size optimization

## Script Locations

The script outputs PDFs to your current working directory. To specify a different location:

```python
output_dir = Path.home() / "Documents" / "offline-docs"
output_dir.mkdir(parents=True, exist_ok=True)
pdf_path = output_dir / f"{output_name}.pdf"
```

## Performance Notes

- Processing time scales with repository size
- Average processing: ~100 markdown files per minute
- Memory usage: ~50MB per 1000 files
- Output size: ~1-5MB per 100 pages

## License

MIT License - Use freely for personal and commercial projects.