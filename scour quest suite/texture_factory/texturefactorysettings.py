import os
import bpy

# Get the path to the directory containing the main script (__init__.py)
addon_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Construct the path to the toolassets.blend file in the addon's root directory
blend_file_path = os.path.join(addon_directory, "toolassets.blend")

with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
        data_to.objects = ["TestObject"]  # Replace with the actual name of the mesh object
for obj in data_to.objects:
    bpy.context.collection.objects.link(obj)



    
