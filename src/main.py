import os
import sys
import shutil
from pathlib import Path
from gencontent import generate_pages_recursive

def main():
    # Get basepath from command line or default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    # Paths
    dir_path_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_path_content = os.path.join(dir_path_root, "content")
    dir_path_docs = os.path.join(dir_path_root, "docs")  # Changed from "public" to "docs"
    template_path = os.path.join(dir_path_root, "template.html")
    dir_path_static = os.path.join(dir_path_root, "static")
    
    # Delete docs directory if it exists
    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)
    
    # Create docs directory
    os.makedirs(dir_path_docs, exist_ok=True)
    
    # Copy static files to docs directory
    print("Copying static files to docs directory...")
    for root, dirs, files in os.walk(dir_path_static):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, dir_path_static)
            dest_path = os.path.join(dir_path_docs, rel_path)
            
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Copy the file
            print(f" * {src_path} -> {dest_path}")
            shutil.copy2(src_path, dest_path)
    
    # Generate content
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)

if __name__ == "__main__":
    main()