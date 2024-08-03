import subprocess

def run_blender_script(description, output_image_path):
    script_path = "render.py"  # Ensure this is the correct path to your render.py
    subprocess.run(["blender", "--background", "--python", script_path, "--", description, output_image_path])

if __name__ == "__main__":
    description = "Example description of floor plan"
    output_image_path = "output_image.png"
    run_blender_script(description, output_image_path)
