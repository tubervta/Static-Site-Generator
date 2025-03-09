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
                # Remove the basepath parameter
                generate_page(from_path, template_path, dest_path)
        else:  # If it's a directory
            os.makedirs(dest_path, exist_ok=True)  # Ensure directory exists
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown file
    with open(from_path, 'r') as file:
        md_content = file.read()
    
    # Read template file
    with open(template_path, 'r') as file:
        template = file.read()
    
    # Convert markdown to HTML using your function
    html_node = markdown_to_html_node(md_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(md_content)
    
    # Replace placeholders
    html = template.replace('{{ Title }}', title)
    html = html.replace('{{ Content }}', html_content)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write output file
    with open(dest_path, 'w') as file:
        file.write(html)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")