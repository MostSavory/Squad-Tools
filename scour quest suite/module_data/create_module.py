import bpy

# Define the set_origin_to_geometry function


def set_origin_to_geometry(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

def CreateModule(module_type, module_name):
    print("Creating module with type:", module_type)
    print("Module name:", module_name)

    # Get the selected objects at the beginning of the script as a list
    selected_objects = list(bpy.context.selected_objects)
    print("Selected objects:", selected_objects)

    # Create a new collection for the selected objects
    new_category = bpy.data.collections.new(module_name)
    bpy.context.scene.collection.children.link(new_category)
    print("Created collection:", module_name)

    # Create subcollections for different object types
    mesh_collection = bpy.data.collections.new("Meshes")
    new_category.children.link(mesh_collection)
    socket_collection = bpy.data.collections.new("Sockets")
    new_category.children.link(socket_collection)
    collision_collection = bpy.data.collections.new("Collision")
    new_category.children.link(collision_collection)
    lods_collection = bpy.data.collections.new("LODs")
    new_category.children.link(lods_collection)
    print("Created subcollections")

    # List to hold the duplicated meshes
    duplicated_meshes = []

    # Iterate through the selected objects
    for obj in selected_objects:
        print("Processing object:", obj.name)

        # Check if the object has the custom property "object Type"
        if "object Type" in obj.keys():
            object_type = obj["object Type"]
            print("Object type:", object_type)

            # Remove the object from its current collections
            for col in obj.users_collection:
                col.objects.unlink(obj)
                print(f"Unlinked object '{obj.name}' from collection '{col.name}'")

            # Move objects with type "Mesh" to the "Meshes" collection
            if object_type == "MESH":
                mesh_collection.objects.link(obj)
                print("Linked object to Meshes collection")

            # Move objects with type "Mesh" to the "Meshes" collection
            elif object_type == "UNHANDLED":
                mesh_collection.objects.link(obj)
                print("Linked object to Meshes collection")

            # Move objects with type "Socket" to the "Sockets" collection
            elif object_type == "SOCKET":
                socket_collection.objects.link(obj)
                print("Linked object to Sockets collection")

            # Move objects with type "Collision" to the "Collision" collection
            elif object_type == "COLLISION":
                collision_collection.objects.link(obj)
                print("Linked object to Collision collection")

            # Move objects with type "LOD" to the "LODs" collection
            elif object_type == "LOD":
                lods_collection.objects.link(obj)
                print("Linked object to LODs collection")

            # Duplicate and link only Blender "Mesh" objects
            if obj.type == "MESH":
                dup_obj = obj.copy()
                new_category.objects.link(dup_obj)  # Link to the NewCategory
                
                duplicated_meshes.append(dup_obj)
                print("Duplicated and linked object")

    try:
        # Join the duplicated meshes into a single "Module Type" mesh
        if duplicated_meshes:
            bpy.context.view_layer.objects.active = duplicated_meshes[0]
            bpy.ops.object.select_all(action='DESELECT')
            for obj in duplicated_meshes:
                obj.select_set(True)
            bpy.ops.object.join()
            print("Joined duplicated meshes")
            # Set the origin to geometry for the merged object

            
            # Set the "object Type" custom property for the module type mesh
            duplicated_meshes[0]["object Type"] = "MODULE"
            print("Set 'object Type' property")

            # Set the "object Type" custom property for the module type mesh
            duplicated_meshes[0]["module Type"] = module_type
            print("Set 'module Type' property")

    except Exception as e:
        print("Error during module creation:", str(e))
        return {'CANCELLED'}  # Or handle the error as needed

    # Parent the objects in subcollections to the module type mesh
    module_mesh = duplicated_meshes[0]
    for subcollection in [mesh_collection, socket_collection, collision_collection, lods_collection]:
        for obj in subcollection.objects:
            obj.select_set(True)
            module_mesh.select_set(True)
            bpy.context.view_layer.objects.active = module_mesh
            bpy.ops.object.parent_set(type='OBJECT')
            print(f"Parented object to {module_mesh.name}")

    # Rename the module type mesh to "Module Name"
    module_mesh.name = module_name
    print("Renamed module type mesh to", module_name)

    # Set the origin to geometry for the merged object (after parenting)
    set_origin_to_geometry(module_mesh)

    return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(CreateModule.bl_idname)

def register():
    bpy.utils.register_class(CreateModule)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(CreateModule)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
