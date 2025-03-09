import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node
import markdown


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)

        # Calculate relative path and build correct destination path
        rel_path = os.path.relpath(from_path, dir_path_content)
        dest_path = os.path.join(dest_dir_path, rel_path)

        print(f"Original path: {from_path}")
        print(f"Generated destination path: {dest_path}")

        if os.path.isfile(from_path):  # If it's a file
            # Only generate HTML for markdown files
            if from_path.endswith(".md"):
                dest_path = Path(dest_path).with_suffix(".html")
                generate_page(from_path, template_path, dest_path, basepath)
        else:  # If it's a directory
            os.makedirs(dest_path, exist_ok=True)  # Ensure directory exists
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def generate_page(md_file_path, template_path, output_file_path, basepath="/"):
    # Ensure basepath is properly formatted (ends with trailing slash)
    if not basepath.endswith('/'):
        basepath += '/'
    
    # Read markdown file
    with open(md_file_path, 'r') as file:
        md_content = file.read()
    
    # Parse markdown to HTML
    md = markdown.Markdown(extensions=['meta'])
    html_content = md.convert(md_content)
    
    # Replace <em> tags with <i> tags for compatibility
    html_content = html_content.replace("<em>", "<i>").replace("</em>", "</i>")
    
    # Get title from metadata or filename
    if hasattr(md, 'Meta') and 'title' in md.Meta and md.Meta['title']:
        title = md.Meta['title'][0]
    else:
        # Fallback to using filename as title
        title = os.path.splitext(os.path.basename(md_file_path))[0]
    
    # Read template
    with open(template_path, 'r') as file:
        template = file.read()
    
    # Replace placeholders
    html = template.replace('{{ Title }}', title)
    html = html.replace('{{ Content }}', html_content)
    
    # Fix the basepath replacement
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    # Write output file
    with open(output_file_path, 'w') as file:
        file.write(html)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")