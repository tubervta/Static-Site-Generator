import os
import shutil
from pathlib import Path
# Import the generate_page function from wherever you've defined it
from gencontent import generate_page  # Replace 'your_module' with the actual module name

def main():
    # Paths - simplified to match the assignment
    dir_path_public = "public"  # Change to public as required
    template_path = "template.html"
    
    # Delete public directory if it exists
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    # Create public directory
    os.makedirs(dir_path_public, exist_ok=True)
    
    # Copy static files to public directory
    if os.path.exists("static"):
        print("Copying static files to public directory...")
        for item in os.listdir("static"):
            source = os.path.join("static", item)
            destination = os.path.join(dir_path_public, item)
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
    
    # Generate index page specifically
    print("Generating page...")
    generate_page(
        "content/index.md",
        template_path,
        os.path.join(dir_path_public, "index.html")
    )

if __name__ == "__main__":
    main()