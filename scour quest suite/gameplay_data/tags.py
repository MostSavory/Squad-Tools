#tags.py
import bpy
import os

# Define the path to the text file for storing the list data
GT_DATA_FILE = os.path.join(os.path.dirname(__file__), "tag_list.txt")

class TagItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    parent: bpy.props.StringProperty()
    show_hierarchy: bpy.props.BoolProperty(default=False)  # Set default value to False

class OBJECT_OT_ToggleHierarchyOperator(bpy.types.Operator):
    bl_idname = "custom.toggle_hierarchy"
    bl_label = "Toggle Hierarchy"
    tag: bpy.props.StringProperty()  # Store the tag name

    def execute(self, context):
        # Find the corresponding tag and toggle its show_hierarchy property
        tag = context.scene.tag_list.get(self.tag)
        if tag:
            tag.show_hierarchy = not tag.show_hierarchy
        return {'FINISHED'}
    
def find_or_create_tag(context, tag_name, parent_tag):
    full_tag_name = tag_name if not parent_tag else f"{parent_tag.name}.{tag_name}"
    tag = context.scene.tag_list.get(full_tag_name)
    
    if not tag:
        tag = context.scene.tag_list.add()
        tag.name = full_tag_name
        tag.parent = parent_tag.name if parent_tag else ""
        
    return tag

class OBJECT_OT_AddTagOperator(bpy.types.Operator):
    bl_idname = "custom.add_tag"
    bl_label = "Add Tag"

    def execute(self, context):
        new_tag = context.scene.new_tag.strip()
        if new_tag:
            tag_parts = new_tag.split('.')
            parent_tag = None

            for tag_part in tag_parts:
                parent_tag = find_or_create_tag(context, tag_part, parent_tag)

            self.save_list_to_file(context)
        return {'FINISHED'}
        

    def save_list_to_file(self, context):
        # Save the list data to the text file
        with open(GT_DATA_FILE, 'w') as f:
            for tag in context.scene.tag_list:
                f.write(tag.name + '\n')

class GameplayTagsPanel(bpy.types.Panel):
    bl_idname = "PT_GameplayTagsPanel"
    bl_label = "Gameplay Tags"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Game Tools'

    def draw(self, context):
        layout = self.layout

        # Draw the hierarchical structure
        self.draw_hierarchy(layout, context, "")

        # Add tag input field
        row = layout.row(align=True)
        row.prop(context.scene, "new_tag", text="New Tag")
        row.operator("custom.add_tag", text="Add Tag")

    def draw_hierarchy(self, layout, context, parent_name):
        sub_tags = [tag for tag in context.scene.tag_list if tag.parent == parent_name]

        for tag in sub_tags:
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)

            row.prop(tag, "show_hierarchy", text=tag.name, emboss=False, icon='TRIA_DOWN' if tag.show_hierarchy else 'TRIA_RIGHT')
            toggle_operator = row.operator("custom.toggle_hierarchy", text="", icon='TRIA_DOWN' if tag.show_hierarchy else 'TRIA_RIGHT')
            toggle_operator.tag = tag.name

            remove_operator = row.operator("custom.remove_tag", text="", icon='X')
            remove_operator.tag = tag.name

            if tag.show_hierarchy:
                self.draw_hierarchy(col, context, tag.name)

class OBJECT_OT_RemoveTagOperator(bpy.types.Operator):
    bl_idname = "custom.remove_tag"
    bl_label = "Remove Tag"
    tag: bpy.props.StringProperty()

    def execute(self, context):
        tag_name = self.tag
        if tag_name:
            # Remove the tag from the text file
            self.remove_tag_from_file(tag_name)
            # Clear and reload the list from the text file
            context.scene.tag_list.clear()
            load_list_data()
        return {'FINISHED'}

    def remove_tag_from_file(self, tag_name):
        lines = []
        if os.path.exists(GT_DATA_FILE):
            with open(GT_DATA_FILE, 'r') as f:
                lines = f.readlines()

        with open(GT_DATA_FILE, 'w') as f:
            for line in lines:
                if line.strip() != tag_name:
                    f.write(line)
        

# Load list data from file if it exists
def load_list_data():
    if os.path.exists(GT_DATA_FILE):
        with open(GT_DATA_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                tag_name = line.strip()
                tag_parts = tag_name.split('.')
                parent_tag = None
                for tag_part in tag_parts:
                    parent_tag = find_or_create_tag(bpy.context, tag_part, parent_tag)

# Register and run the script
def register():
    bpy.utils.register_class(GameplayTagsPanel)
    bpy.utils.register_class(OBJECT_OT_AddTagOperator)
    bpy.utils.register_class(OBJECT_OT_ToggleHierarchyOperator)
    bpy.utils.register_class(OBJECT_OT_RemoveTagOperator)
    bpy.utils.register_class(TagItem)

    bpy.types.Scene.tag_list_index = bpy.props.IntProperty()
    bpy.types.Scene.new_tag = bpy.props.StringProperty()
    bpy.types.Scene.tag_list = bpy.props.CollectionProperty(type=TagItem)
    load_list_data()

def unregister():
    bpy.utils.unregister_class(GameplayTagsPanel)
    bpy.utils.unregister_class(OBJECT_OT_AddTagOperator)
    bpy.utils.unregister_class(OBJECT_OT_ToggleHierarchyOperator)
    bpy.utils.unregister_class(OBJECT_OT_RemoveTagOperator)
    bpy.utils.unregister_class(TagItem)
    del bpy.types.Scene.tag_list 

if __name__ == "__main__":
    register()