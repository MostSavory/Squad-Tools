

#toolsmain.py
import os
import bpy
from mathutils import Vector
from . module_data import edit_sockets
from . module_data import edit_collision
from . module_data import edit_lods
from .sprite_shoppe import spritesettings
from . module_data import edit_masks
from .texture_factory import texturefactorysettings
from .gameplay_data import edit_gameplay_data
from .module_data import edit_object_data


#check if dat is being edited
def is_data_being_edited():
    return (
        edit_sockets.PrefabPanel.is_registered
        or edit_collision.CollisionPanel.is_registered
        or edit_lods.LODPanel.is_registered
        or edit_masks.MasksPanel.is_registered
    )

######## Tool Menu #####################################################################################################################################


class OpenTextureFactory(bpy.types.Operator):
    bl_idname = "object.texture_factory"
    bl_label = "Texture Factory"

    def execute(self, context):
        texturefactorysettings.register()
        return {'FINISHED'}


class SpriteShoppe(bpy.types.Operator):
    bl_idname = "object.sprite_shoppe"
    bl_label = "Sprite Shoppe"

    def execute(self, context):
        # Check if the `ToolPanel` class is registered.
        if spritesettings.SpriteShoppePanel.is_registered:
            print("The `ToolPanel` class is registered.")
        else:
            print("The `ToolPanel` class is not registered.")
            spritesettings.register()
        return {'FINISHED'}


class EditGameplayeditgameplaydata(bpy.types.Operator):
    bl_idname = "object.edit_gameplay_editgameplaydata"
    bl_label = "Data Settings"

    def execute(self, context):
        edit_gameplay_data.register()
        return {'FINISHED'}


class ModularPreview(bpy.types.Operator):
    bl_idname = "object.modular_preview"
    bl_label = "Modular Preview"

    def execute(self, context):
        pass
        return {'FINISHED'}


class ToolPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_Toolbelt"
    bl_label = "Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Game Tools"


    #check if editing a prefab/mesh data
    @classmethod
    def poll(cls, context):
        if is_data_being_edited():
            return False
        else:
            return not bpy.context.selected_objects


    def draw(self, context):

        layout = self.layout
        obj = context.object
    
        row = layout.row()
        row.operator("object.modular_preview", text="Modular Previewer")
        row = layout.row()
        row.operator("object.sprite_shoppe", text="Sprite Shoppe")
        row = layout.row()
        row.operator("object.texture_factory", text="Texture Factory")
        row = layout.row()
        row.operator("object.edit_gameplay_editgameplaydata", text="Data Settings")


######## Active Module Menu #######################################################################################################################


#edit metafab

class EditCollision(bpy.types.Operator):
    bl_idname = "object.edit_collision"
    bl_label = "Edit Collision"

    def execute(self, context):
        # Check if the `ToolPanel` class is registered.
        if edit_collision.CollisionPanel.is_registered:
            print("The `ToolPanel` class is registered.")
        else:
            print("The `ToolPanel` class is not registered.")
            edit_collision.register()
        return {'FINISHED'}


class EditCollision(bpy.types.Operator):
    bl_idname = "object.edit_collision"
    bl_label = "Edit Collision"

    def execute(self, context):
        # Check if the `ToolPanel` class is registered.
        if edit_collision.CollisionPanel.is_registered:
            print("The `ToolPanel` class is registered.")
        else:
            print("The `ToolPanel` class is not registered.")
            edit_collision.register()
        return {'FINISHED'}
    

class EditLODs(bpy.types.Operator):
    bl_idname = "object.edit_lods"
    bl_label = "Edit LODs"


    def execute(self, context):
        # Check if the `ToolPanel` class is registered.
        if edit_lods.LODPanel.is_registered:
            print("The `ToolPanel` class is registered.")
        else:
            print("The `ToolPanel` class is not registered.")
            edit_lods.register()
        return {'FINISHED'}


class EditMasks(bpy.types.Operator):
    bl_idname = "object.edit_masks"
    bl_label = "Edit Masks"

    def execute(self, context):
        # Check if the `ToolPanel` class is registered.
        if edit_masks.MasksPanel.is_registered:
            print("The `ToolPanel` class is registered.")
        else:
            print("The `ToolPanel` class is not registered.")
            edit_masks.register()
        return {'FINISHED'}


class EditSockets(bpy.types.Operator):
    bl_idname = "object.edit_sockets"
    bl_label = "Edit Sockets"

    def execute(self, context):

        # Check if the `ToolPanel` class is registered.
        if edit_sockets.PrefabPanel.is_registered:
            print("The `ToolPanel` class is registered.")
        else:
            print("The `ToolPanel` class is not registered.")
            edit_sockets.register()
        return {'FINISHED'}


class ModulePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_ModulePanel"
    bl_label = "Selected Module"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Game Tools"

#check if editing a prefab/mesh data
    @classmethod
    def poll(cls, context):
        if is_data_being_edited() and len(bpy.context.selected_objects) < 1:
            return False

        if not context.selected_objects:
            return False

        if any(obj.get('module Type', '').lower() == 'unhandled' for obj in context.selected_objects) or any(obj.get('module Type', '').lower() == 'metafab' for obj in context.selected_objects):
            return False

        return True


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object

        row = layout.row()
        row.operator("object.edit_sockets")
        row = layout.row()
        row.operator("object.edit_collision")
        row = layout.row()
        row.operator("object.edit_lods")
        
        row = layout.row()
        row.operator("object.edit_masks")
        row = layout.row()



######## Unreal Menu ###########################################################################################################################

class UpdateAll(bpy.types.Operator):
    bl_idname = "object.export_all"
    bl_label = "Update All"

    def execute(self, context):
        script_path = os.path.join(os.path.dirname(__file__), "communication", "rpc", "uexportdatatables.py")
        
        with open(script_path, "r") as script_file:
            script_content = script_file.read()
            
        try:
            #blenderserver.send_script_to_unreal(script_content)
            print("begin.")
        except Exception as e:
            print("Error sending script:")

        return {'FINISHED'}


class ExportSelected(bpy.types.Operator):
    bl_idname = "object.export_selected"
    bl_label = "Export Selected"

    def execute(self, context):
        #editcollision.register()
        pass
        return {'FINISHED'}


class ExportPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_Unreal"
    bl_label = "Unreal Engine"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Game Tools"

    #check if editing a prefab/mesh data
    @classmethod
    def poll(cls, context):
        if is_data_being_edited():
            return False
        else:
            return True
    
    def draw(self, context):
        layout = self.layout
        obj = context.object

        #Check if an object is selected
        if bpy.context.selected_objects:
            row = layout.row()
            row.operator("object.export_selected", text="Export Selected")
        else:
            pass

        row = layout.row()
        row.operator("object.export_all", text="Export All")


def register():

    edit_object_data.register()
    bpy.utils.register_class(ModulePanel)
    bpy.utils.register_class(ToolPanel)
    bpy.utils.register_class(ExportPanel)
    bpy.utils.register_class(EditSockets)
    bpy.utils.register_class(EditCollision)
    bpy.utils.register_class(EditLODs)
    bpy.utils.register_class(EditMasks)
    bpy.utils.register_class(SpriteShoppe)
    bpy.utils.register_class(OpenTextureFactory)
    bpy.utils.register_class(EditGameplayeditgameplaydata)
    bpy.utils.register_class(ModularPreview)
    bpy.utils.register_class(ExportSelected)
    bpy.utils.register_class(UpdateAll)

    # Name of the target addon you want to reference
    send2ue = "send2ue"
    # Check if the target addon is enabled
    if send2ue in bpy.context.preferences.addons:
        try:
            # Import modules from the target addon
            from send2ue import operators

            print("Success")

        except ImportError:

            print("Import Failed")

            pass

    else:
        print("Send2UE not enabled")  # Handle the case where the target addon is not enabled
        pass

def unregister():

    bpy.utils.unregister_class(edit_object_data)   
    bpy.utils.unregister_class(ModulePanel)
    bpy.utils.unregister_class(ToolPanel)
    bpy.utils.unregister_class(ExportPanel)
    bpy.utils.unregister_class(EditSockets)
    bpy.utils.unregister_class(EditCollision)
    bpy.utils.unregister_class(EditLODs)
    bpy.utils.unregister_class(EditMasks)
    bpy.utils.unregister_class(SpriteShoppe)
    bpy.utils.unregister_class(OpenTextureFactory)
    bpy.utils.unregister_class(EditGameplayeditgameplaydata)
    bpy.utils.unregister_class(ModularPreview)
    bpy.utils.unregister_class(ExportSelected)
    bpy.utils.unregister_class(UpdateAll)
    del bpy.types.Object.Module_type

if __name__ == "__main__":
    register()
    