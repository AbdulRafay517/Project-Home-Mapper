import bpy
import sys
import os

def create_3d_floor_plan(description):
    # Create a floor
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Floor"
    
    # Example: adding walls around the floor
    wall_height = 2.5
    wall_thickness = 0.2
    
    # Add four walls
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 5, wall_height / 2))
    wall1 = bpy.context.object
    wall1.scale = (5, wall_thickness, wall_height / 2)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -5, wall_height / 2))
    wall2 = bpy.context.object
    wall2.scale = (5, wall_thickness, wall_height / 2)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(5, 0, wall_height / 2))
    wall3 = bpy.context.object
    wall3.scale = (wall_thickness, 5, wall_height / 2)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-5, 0, wall_height / 2))
    wall4 = bpy.context.object
    wall4.scale = (wall_thickness, 5, wall_height / 2)
    
    # Add a roof
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, wall_height))
    roof = bpy.context.object
    roof.name = "Roof"

def render_floor_plan(output_path):
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    description = sys.argv[-2]  # Description from command line argument
    output_image_path = sys.argv[-1]  # Output image path from command line argument
    create_3d_floor_plan(description)
    render_floor_plan(output_image_path)
