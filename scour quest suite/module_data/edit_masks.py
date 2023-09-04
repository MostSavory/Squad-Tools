import bpy

class SaveMasks(bpy.types.Operator):
    bl_idname = "object.save_masks"
    bl_label = "Save Masks"

    def execute(self, context):
        unregister()
        
        return {'FINISHED'}
    
    
class SetColorOperator(bpy.types.Operator):
    bl_idname = "object.set_color"
    bl_label = "Set Object Color"

    color: bpy.props.FloatVectorProperty()

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':
                obj.color = self.color
        return {'FINISHED'}


class MasksPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_EditMasks"
    bl_label = "Vertex Painting"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Game Tools"

    def draw(self, context):
        layout = self.layout
        obj = context.object


        row = layout.row()
        row.operator("object.save_masks", text="Save Masks")

        row = layout.row()
        row.label(text="Colors:")
        row.operator("object.set_color", text="Red").color = (1, 0, 0,)


def register():
    #bpy.utils.register_class(ToolPanel)
    bpy.utils.register_class(MasksPanel)
    bpy.utils.register_class(SaveMasks)
    bpy.utils.register_class(SetColorOperator)
    bpy.types.Scene.selected_image = bpy.props.StringProperty()   
    
 
def unregister():
    #bpy.utils.unregister_class(ToolPanel)
    bpy.utils.unregister_class(MasksPanel)
    bpy.utils.unregister_class(SaveMasks)
    bpy.utils.unregister_class(SetColorOperator)
    del bpy.types.Scene.selected_image

if __name__ == "__main__":
    register()

