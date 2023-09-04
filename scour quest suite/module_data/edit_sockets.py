#prefabsettings.py
import bpy

class SaveExit(bpy.types.Operator):
    bl_idname = "object.save_exit"
    bl_label = "Save Exit"

    def execute(self, context):
        unregister()
        return {'FINISHED'}

class PrefabPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_Prefab_Data"
    bl_label = "Prefab Data"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Game Tools"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        row = layout.row()
        row.operator("object.save_exit", text="Save Data")
        row = layout.row()

def register():
    bpy.utils.register_class(PrefabPanel)
    bpy.utils.register_class(SaveExit)

def unregister():
    bpy.utils.unregister_class(PrefabPanel)
    bpy.utils.unregister_class(SaveExit)
    
if __name__ == "__main__":
    register()