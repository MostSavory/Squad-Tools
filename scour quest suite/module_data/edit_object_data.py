#edit_object_data.py
import bpy
from . import create_module

# Define a custom property to track dropdown selection
bpy.types.Scene.is_dropdown_selection = bpy.props.BoolProperty(default=False)

# List of object types
object_types = [
    ("UNHANDLED", "Unhandled", "Unhandled"),  # Default option
    ("SOCKET", "Socket", "Socket Type"),
    ("MESH", "Mesh", "Mesh Type"),  # Add Mesh object type
]

# List of collision types
collision_types = [
    ("DEFAULT_CONVEX", "Default (Convex)", "Default (Convex)"),
    ("FLAT_HORIZONTAL", "Flat Horizontal", "Flat Horizontal"),
    ("FLAT_VERTICAL", "Flat Vertical", "Flat Vertical"),
    ("LITTER", "Litter", "Litter"),
]

# List of module types
module_types = [
    ("UNHANDLED", "Unhandled", "Unhandled"),  # Default option    
    ("DOOR", "Door", "Door module"),
    ("DOORWAY", "Doorway", "Doorway module"),
    ("LOOT_SPAWNER", "Loot Spawner", "Loot Spawner module"),
    ("MOB_SPAWNER", "Mob Spawner", "Mob Spawner module"),
]

# Set custom property on all selected objects
def set_object_prop(value):
    if bpy.context.scene.is_dropdown_selection:
        for obj in bpy.context.selected_objects:
            obj['object Type'] = value

# Get current value
def get_object_prop(obj):
    try:
        if 'object Type' in obj:
            return obj['object Type']
        else:
            return 'UNHANDLED'  # Default object type
    except Exception as e:
        print(f"Error while getting 'object Type' property: {e}")
        return 'UNHANDLED'

# Set custom property for collision type
def set_collision_prop(value):
    if bpy.context.scene.is_dropdown_selection:
        for obj in bpy.context.selected_objects:
            obj['collision Type'] = value

# Get current collision value
def get_collision_prop(obj):
    try:
        if 'collision Type' in obj:
            return obj['collision Type']
        else:
            return 'DEFAULT_CONVEX'  # Default collision type
    except Exception as e:
        print(f"Error while getting 'collision Type' property: {e}")
        return 'DEFAULT_CONVEX'


# Set custom property for module type
def set_module_prop(value):
    if bpy.context.scene.is_dropdown_selection:
        for obj in bpy.context.selected_objects:
            obj['module Type'] = value

# Get current module value
def get_module_prop(obj):
    try:
        if 'module Type' in obj:
            return obj['module Type']
        else:
            return 'UNHANDLED'  # Default module type
    except Exception as e:
        print(f"Error while getting 'module Type' property: {e}")
        return 'UNHANDLED'

# Update selected objects and the object dropdown
def update_object_dropdown(self, context):
    try:
        value = self.object_dropdown
        set_object_prop(value)

        # Update the active object's custom property directly
        if bpy.context.active_object:
            bpy.context.active_object['object Type'] = value
    except Exception as e:
        print(f"Error while updating object dropdown: {e}")

# Update selected objects and the collision dropdown
def update_collision_dropdown(self, context):
    try:
        value = self.collision_dropdown
        set_collision_prop(value)

        # Update the active object's custom property directly
        if bpy.context.active_object:
            bpy.context.active_object['collision Type'] = value
    except Exception as e:
        print(f"Error while updating collision dropdown: {e}")

# Update selected objects and the module dropdown
def update_module_dropdown(self, context):
    try:
        value = self.module_dropdown
        set_module_prop(value)

        # Update the active object's custom property directly
        if bpy.context.active_object:
            bpy.context.active_object['module Type'] = value
    except Exception as e:
        print(f"Error while updating module dropdown: {e}")

# Handler for selection changes due to dropdown selection
def on_dropdown_selection_change(self, context):
    try:
        if bpy.context.active_object:
            bpy.context.scene.object_dropdown = get_object_prop(bpy.context.active_object)
            bpy.context.scene.collision_dropdown = get_collision_prop(bpy.context.active_object)
            module_type = get_module_prop(bpy.context.active_object)
            if module_type in [opt[0] for opt in module_types]:
                bpy.context.scene.module_dropdown = module_type
            else:
                # Instead of raising an error, just leave the module dropdown as it is
                pass
            bpy.context.scene.is_dropdown_selection = True  # Set flag to indicate dropdown selection
    except Exception as e:
        # Instead of printing an error, just leave the module dropdown as it is
        pass

# Handler for selection changes due to other actions (e.g., manual selection)
def on_manual_selection_change(self, context):
    try:
        if not bpy.context.scene.is_dropdown_selection:
            selected_objects = bpy.context.selected_objects

            # Check if any selected objects have the "Prefab" property (case-insensitive)
            has_prefab_properties = any(obj.get('module Type', '').lower() == 'prefab' for obj in selected_objects)

            # Check if any selected objects have the "Metafab" property (case-insensitive)
            has_metafab_properties = any(obj.get('module Type', '').lower() == 'metafab' for obj in selected_objects)

            # Check if all selected objects have the "Prefab" property (case-insensitive)
            all_prefab_properties = all(obj.get('module Type', '').lower() == 'prefab' for obj in selected_objects)

            # Display "Create Prefab" button and text input when conditions are met
            if not has_prefab_properties and not has_metafab_properties and len(selected_objects) >= 2:
                if bpy.context.active_object:
                    bpy.context.scene.object_dropdown = get_object_prop(bpy.context.active_object)
                    bpy.context.scene.collision_dropdown = get_collision_prop(bpy.context.active_object)
                    module_type = get_module_prop(bpy.context.active_object)
                    if module_type in [opt[0] for opt in module_types]:
                        bpy.context.scene.module_dropdown = module_type
                    else:
                        # Instead of raising an error, just leave the module dropdown as it is
                        pass
    except Exception as e:
        # Instead of printing an error, just leave the module dropdown as it is
        pass


    # Reset the flag for dropdown selection
    bpy.context.scene.is_dropdown_selection = False

# Operator to select similar meshes based on vertex count
class SelectSimilarMeshes(bpy.types.Operator):
    bl_idname = "object.select_similar_meshes"
    bl_label = "Select Similar Meshes"

    def execute(self, context):
        active_obj = context.active_object

        if active_obj and active_obj.type == 'MESH':
            active_vertex_count = len(active_obj.data.vertices)

            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

            # Select objects with the same vertex count
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH' and len(obj.data.vertices) == active_vertex_count:
                    obj.select_set(True)

        return {'FINISHED'}
    


# Panel
class ObjectDataPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_CUSTOM"
    bl_label = "Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Game Tools"

    #check if object is selected
    @classmethod
    def poll(cls, context):
            if not context.selected_objects:
                return False

            return True


    def draw(self, context):
        layout = self.layout
        selected_objects = bpy.context.selected_objects

        # Check if any selected objects have the "PREFAB" or "METAFAB" module type (case-insensitive)
        has_prefab_or_metafab = any(
            obj.get('module Type', '').lower() in {'prefab', 'metafab'} for obj in selected_objects
        )

        # Check if the active object's module type is "Module"
        is_object_type_module  = any(
            obj.get('object Type', '').lower() in {'module'} for obj in selected_objects
        )
        # Display object_dropdown if module Type is "UNHANDLED" and no PREFAB or METAFAB
        if not has_prefab_or_metafab and len(selected_objects) >= 1 and not is_object_type_module and not is_object_type_module:
            layout.label(text="Object Data")
            layout.prop(context.scene, "object_dropdown", text="")

        # Display module_dropdown if object Type is "Socket" and no PREFAB or METAFAB
        if not has_prefab_or_metafab and len(selected_objects) >= 1 and bpy.context.active_object and not is_object_type_module:
            if bpy.context.active_object.get('object Type', '').lower() == 'socket':
                layout.label(text="Module Type")
                layout.prop(context.scene, "module_dropdown", text="")

        # Display collision_dropdown if object Type is "MESH" and no PREFAB or METAFAB
        if not has_prefab_or_metafab and len(selected_objects) >= 1 and not is_object_type_module:
            if bpy.context.active_object and bpy.context.active_object.get('object Type', '').lower() == 'mesh':
                layout.label(text="Collision Type")
                layout.prop(context.scene, "collision_dropdown", text="")

        if len(selected_objects) >= 1:
            layout.row().separator()
            layout.operator("object.select_similar_meshes", text="Select Similar Meshes")
            layout.row().separator()

        # Create New panel
        layout = self.layout
        box = layout.box()
        box.label(text="Create New")

        if len(selected_objects) >= 0:
            box.prop(context.scene, "object_name", text="")

        # Create Module button (visible unless no objects are selected, module type is "PREFAB" or "METAFAB", or object type is "Module")
        if len(selected_objects) > 0 and not has_prefab_or_metafab and not is_object_type_module:
            box.prop(context.scene, "create_module_dropdown", text="")
            box.operator("object.create_module_button", text="Create Module")

        # Create Prefab area (hidden if PREFAB or METAFAB is selected or object type is "Module")
        if not has_prefab_or_metafab and len(selected_objects) >= 2:
            box.operator("object.create_prefab_button", text="Create Prefab")

        # Create Metafab area (hidden if no PREFABs are selected or object type is "Module")
        if len(selected_objects) >= 2 and all('module Type' in obj and obj['module Type'].lower() == 'prefab' for obj in selected_objects):
            box.operator("object.create_metafab_button", text="Create Metafab")




        box = layout.box()

        # Iterate through selected objects and display their properties
        for obj in context.selected_objects:
            row = box.row()
            row.label(text=f"{obj.name}| {get_object_prop(obj)}") #  | {get_module_prop(obj)} | {get_collision_prop(obj)}")

# Operator to create a Prefab
class CreatePrefabButton(bpy.types.Operator):
    bl_idname = "object.create_prefab_button"
    bl_label = "Create Prefab"

    def execute(self, context):
        object_name = context.scene.object_name
        if object_name:
            # Your code to create a Prefab with the given name
            print(f"Creating Prefab: {object_name}")
        else:
            print("Prefab Name is empty. Please enter a name.")

        return {'FINISHED'}
    
# Operator to create a Metafab
class CreateMetafabButton(bpy.types.Operator):
    bl_idname = "object.create_metafab_button"
    bl_label = "Create Metafab"

    def execute(self, context):
        metafab_name = context.scene.object_name
        if metafab_name:
            # Your code to create a Metafab with the given name
            print(f"Creating Metafab: {metafab_name}")
        else:
            print("Metafab Name is empty. Please enter a name.")

        return {'FINISHED'}

# Operator to create a Module
class CreateModuleButton(bpy.types.Operator):
    bl_idname = "object.create_module_button"
    bl_label = "Create Module"

    def execute(self, context):
        module_type = context.scene.create_module_dropdown  # Get the selected module type from the button's dropdown
        object_name = context.scene.object_name  # Get the object name from scene property
        if object_name:
            # Override the scene properties temporarily for the execution of the operator
            context.scene['module Type'] = module_type
            context.scene['module_name'] = object_name
            create_module.CreateModule(module_type=module_type, module_name=object_name)  # Call the CreateModule operator using bpy.ops
            print(f"Creating Module: {object_name} of Type: {module_type}")
        else:
            print("Module Name is empty. Please enter a name.")

        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)  # Force a redraw of the Blender UI

        return {'FINISHED'}



def register():
    bpy.utils.register_class(ObjectDataPanel)
    bpy.utils.register_class(SelectSimilarMeshes)
    bpy.utils.register_class(CreateModuleButton)
    bpy.utils.register_class(CreatePrefabButton)
    bpy.utils.register_class(CreateMetafabButton)
    
    # Define object_dropdown
    bpy.types.Scene.object_dropdown = bpy.props.EnumProperty(
        items=[(opt[0], opt[1], opt[2]) for opt in object_types],
        update=update_object_dropdown,
        default=get_object_prop(bpy.context.active_object)  # Set default to active object's object prop
    )

    # Define collision_dropdown
    bpy.types.Scene.collision_dropdown = bpy.props.EnumProperty(
        items=[(opt[0], opt[1], opt[2]) for opt in collision_types],
        update=update_collision_dropdown,
        default=get_collision_prop(bpy.context.active_object)  # Set default to active object's collision prop
    )

    # Define module_dropdown
    bpy.types.Scene.module_dropdown = bpy.props.EnumProperty(
        items=[(opt[0], opt[1], opt[2]) for opt in module_types],
        update=update_module_dropdown,
        default=get_module_prop(bpy.context.active_object)  # Set default to active object's module prop
    )
    #Create module Dropdown
    bpy.types.Scene.create_module_dropdown = bpy.props.EnumProperty(
        items=[(opt[0], opt[1], opt[2]) for opt in module_types]
    )

    # Define custom properties for prefab and metaprefab
    bpy.types.Scene.object_name = bpy.props.StringProperty(
        name="Prefab Name",
        default=""
    )

    # Register the selection change handlers
    bpy.app.handlers.depsgraph_update_post.append(on_manual_selection_change)
    bpy.app.handlers.depsgraph_update_post.append(on_dropdown_selection_change)  # Use depsgraph_update_post here

def unregister():
    bpy.utils.unregister_class(ObjectDataPanel)
    bpy.utils.unregister_class(SelectSimilarMeshes)
    bpy.utils.unregister_class(CreateModuleButton)

    del bpy.types.Scene.object_dropdown
    del bpy.types.Scene.collision_dropdown
    del bpy.types.Scene.module_dropdown
    del bpy.types.Scene.object_name

    # Remove the selection change handler
    bpy.app.handlers.depsgraph_update_post.remove(on_manual_selection_change)
    bpy.app.handlers.depsgraph_update_post.remove(on_dropdown_selection_change)
    del bpy.types.Scene.is_dropdown_selection

if __name__ == "__main__":
    register()
