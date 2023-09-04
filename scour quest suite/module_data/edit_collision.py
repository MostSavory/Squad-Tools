import bpy

class SaveCollision(bpy.types.Operator):
    bl_idname = "object.save_collisions"
    bl_label = "Save Collision"

    def execute(self, context):
        unregister()
        
        return {'FINISHED'}

class AutoGenerate(bpy.types.Operator):
    bl_idname = "object.create_box"
    bl_label = "Create Box"

    def execute(self, context):
        name = "poop"
        create_box(context, name)
        return {'FINISHED'}

class OBJECT_OT_CreateBox(bpy.types.Operator):
    bl_idname = "object.create_box"
    bl_label = "Create Box"

    def execute(self, context):
        name = "poop"
        create_box(context, name)
        return {'FINISHED'}

class OBJECT_OT_CreateConvexHull(bpy.types.Operator):
    bl_idname = "object.create_convex_hull"
    bl_label = "Create Convex Hull"

    def execute(self, context):
        name = "poop"
        create_convex_hull(context, name)
        return {'FINISHED'}

class OBJECT_OT_CreateSphere(bpy.types.Operator):
    bl_idname = "object.create_sphere"
    bl_label = "Create Sphere"

    def execute(self, context): 
        name = "poop"
        create_sphere(context, name)
        return {'FINISHED'}

def create_box(context, name):
    selected_object = bpy.context.selected_objects[0]
    obj = context.object
    apply_transforms(obj)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

    # Create the bounding box
    bpy.ops.mesh.primitive_cube_add()
    bounding_box_object = bpy.context.active_object

    # Set the dimensions and location of the bounding box to match the selected object
    bounding_box_object.dimensions = selected_object.dimensions
    bounding_box_object.location = selected_object.location

    # Update the viewport to reflect the changes
    bpy.context.view_layer.update()

    # Find objects with the same name
    same_name_objects = [o for o in bpy.data.objects if o.name.startswith(f"UBX_{name}")]

    # Generate the sequential numbering
    numbering = 1
    for o in same_name_objects:
        if o != bounding_box_object:
            numbering += 1

    # Format the numbering with leading zeros
    numbering_str = f"{numbering:02d}"

    bounding_box_object.name = f"UBX_{name}_{numbering_str}"

def create_convex_hull(context, name):
    bpy.ops.object.duplicate()
    obj = context.object
    apply_transforms(obj)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.convex_hull()
    bpy.ops.object.mode_set(mode='OBJECT')

    # Find objects with the same name
    same_name_objects = [o for o in bpy.data.objects if o.name.startswith(f"UCX_{name}")]

    # Generate the sequential numbering
    numbering = 1
    for o in same_name_objects:
        if o != obj:
            numbering += 1

    # Format the numbering with leading zeros
    numbering_str = f"{numbering:02d}"

    obj.name = f"UCX_{name}_{numbering_str}"
    
def create_sphere(context, name):
    active_object = bpy.context.active_object
    obj = context.object
    apply_transforms(obj)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

    # Create the sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8)

    # Get the newly created sphere object
    sphere = bpy.context.active_object

    # Set the location of the sphere to match the active object
    sphere.location = active_object.location

    # Get the maximum dimension of the 'obj' object
    max_dim = max(obj.dimensions) / 2

    # Set the radius of the sphere to match the maximum dimension of the 'obj' object
    sphere.scale = (max_dim, max_dim, max_dim)

    # Update the viewport to reflect the changes
    bpy.context.view_layer.update()

    # Find objects with the same name
    same_name_objects = [o for o in bpy.data.objects if o.name.startswith(f"USP_{name}")]

    # Generate the sequential numbering
    numbering = 1
    for o in same_name_objects:
        if o != sphere:
            numbering += 1

    # Format the numbering with leading zeros
    numbering_str = f"{numbering:02d}"

    sphere.name = f"USP_{name}_{numbering_str}"

def apply_transforms(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

class CollisionPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_Export"
    bl_label = "Collision"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Game Tools"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.operator("object.save_collisions", text="Save Collision")
        row = layout.row()
        row.operator("object.create_box", text="Create Box")
        row = layout.row()
        row.operator("object.create_convex_hull", text="Create Convex")
        row = layout.row()
        row.operator("object.create_sphere", text="Create Sphere")
        row = layout.row()

def register():
    #bpy.utils.register_class(ToolPanel)
    bpy.utils.register_class(CollisionPanel)
    bpy.utils.register_class(SaveCollision)
    bpy.utils.register_class(OBJECT_OT_CreateBox)
    bpy.utils.register_class(OBJECT_OT_CreateConvexHull)
    bpy.utils.register_class(OBJECT_OT_CreateSphere)

def unregister():
    #bpy.utils.unregister_class(ToolPanel)
    bpy.utils.unregister_class(CollisionPanel)
    bpy.utils.unregister_class(SaveCollision)
    bpy.utils.unregister_class(OBJECT_OT_CreateBox)
    bpy.utils.unregister_class(OBJECT_OT_CreateConvexHull)
    bpy.utils.unregister_class(OBJECT_OT_CreateSphere)

if __name__ == "__main__":
    register()



