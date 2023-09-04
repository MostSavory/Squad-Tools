import bpy
from . import tags
import os



class EditGameDataProperties(bpy.types.PropertyGroup):
    unreal_project_directory: bpy.props.StringProperty(
        name="Unreal Project Directory",
        description="Select the directory of your Unreal project",
        subtype='DIR_PATH'
    )

class ImportUnrealTags(bpy.types.Operator):
    bl_idname = "object.import_unreal_tags"
    bl_label = "Import Unreal Tags"

    def execute(self, context):
        #run uImportUnrealTags
        
        pass
        return {'FINISHED'}

class EditDataPanel(bpy.types.Panel):
    bl_idname = "PT_EditDataPanel"
    bl_label = "Game Data"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Game Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Display the Unreal project directory selector
        row = layout.row()
        row.prop(scene.edit_game_data_props, "unreal_project_directory")
        
        # Add tag input field
        row = layout.row()
        row.operator("object.import_unreal_tags", text="Import Unreal Tags")

def register():
    bpy.utils.register_class(EditDataPanel)
    bpy.utils.register_class(ImportUnrealTags)    
    bpy.utils.register_class(EditGameDataProperties)
    bpy.types.Scene.edit_game_data_props = bpy.props.PointerProperty(type=EditGameDataProperties)
    tags.register()

def unregister():
    bpy.utils.unregister_class(EditDataPanel)
    bpy.utils.unregister_class(ImportUnrealTags)    
    bpy.utils.unregister_class(EditGameDataProperties)
    del bpy.types.Scene.edit_game_data_props

if __name__ == "__main__":
    register()
