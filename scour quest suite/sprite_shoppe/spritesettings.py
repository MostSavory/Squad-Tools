import bpy
import os
import subprocess
from . import createspritesheet
from . import setupspritescene
from . import spritetemplates

#calculate final resolution
def calculate_final_resolution(down_resolution, total_frames, square_sprite_sheet):
    final_width = down_resolution[0] * total_frames

    if square_sprite_sheet:
        rows = int((total_frames ** 0.5).is_integer() and (total_frames ** 0.5) or (total_frames ** 0.5 // 1) + 1)
        width_for_square = max(down_resolution[0], down_resolution[1])
        final_width = width_for_square * rows
        final_height = width_for_square * rows
    else:
        final_height = down_resolution[1]

    return final_width, final_height


def update_resolution(self, context):
    render_settings = context.scene.render
    render_settings.resolution_x = self.frame_resolution[0]
    render_settings.resolution_y = self.frame_resolution[1]
    

def set_custom_frame_rate(self, context):
    # Switch to "Custom" frame rate mode
    context.scene.render.fps_base = 1
    context.scene.render.fps = self.frame_rate


# OPERATOR templates
class CreateSpriteSheetOperator(bpy.types.Operator):
    bl_idname = "object.create_sprite_sheet"
    bl_label = "Create Sprite Sheet"
    
    def execute(self, context):
        # Add code for the action to be performed when the button is clicked
        self.report({'INFO'}, "Create Sprite Sheet button was clicked!")
        
        createspritesheet()
        
        return {'FINISHED'}
    
      

# OPERATOR templates
class TemplatesOperator(bpy.types.Operator):
    bl_idname = "object.templates"
    bl_label = "Templates"
    
    def execute(self, context):
        # Add code for the action to be performed when the button is clicked
        self.report({'INFO'}, "Templates button was clicked!")
        
        spritetemplates()
        
        return {'FINISHED'}
    
    # OPERATOR set up scene
class SetUpSceneOperator(bpy.types.Operator):
    bl_idname = "object.set_up_scene"
    bl_label = "Set up scene"
    
    def execute(self, context):
        # add code for scene set up here
        self.report({'INFO'}, "Scene set up!")
        
        setupspritescene()
        
        return {'FINISHED'}



# Operator to reverse frames
class ReverseOperator(bpy.types.Operator):
    bl_idname = "object.reverse"
    bl_label = "Reverse"

    reverse: bpy.props.BoolProperty(name="Reverse")
    def execute(self, context):
        # Add code to reverse frames here
        self.report({'INFO'}, "Frames reversed!")
        return {'FINISHED'}
    

class BakeAllOperator(bpy.types.Operator):
    bl_idname = "object.bake_all"
    bl_label = "Bake All"

    def execute(self, context):
        # Iterate through all objects in the scene
        for obj in bpy.context.scene.objects:
            # Check if the object is a fluid domain
            if obj.type == 'MESH' and obj.modifiers:
                fluid_modifier = None
                # Find the fluid modifier attached to the domain object
                for modifier in obj.modifiers:
                    if modifier.type == 'FLUID' and modifier.fluid_type == 'DOMAIN':
                        fluid_modifier = modifier
                        
                # If there's a fluid modifier, bake the fluid simulation
                if fluid_modifier:
                    print("Baking fluid for", obj.name)
                    # Select the domain object and set it as active
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj

                    # Switch to the correct mode for baking (e.g., OBJECT or EDIT mode)
                    # If needed, you may add a check here to switch to the appropriate mode
                    # bpy.ops.object.mode_set(mode='OBJECT')

                    # Start baking the fluid simulation
                    bpy.ops.ptcache.bake_all(bake=True)

                    # Deselect the object after baking
                    obj.select_set(False)

        return {'FINISHED'}




# UI panel to display the button and customization options
class SpriteShoppePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_sprite_shoppe"
    bl_label = "Sprite Shoppe"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Scour/Quest tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("object.templates", text="Templates", icon='SCENE_DATA')
        layout.separator()
        layout.operator("object.set_up_scene", text="Set up current scene", icon='SCENE')
        layout.separator()
        total_frames = scene.non_blended_frames + scene.blended_frames + scene.blank_frames
        layout.label(text=f"Total Frames: {total_frames}")
        layout.prop(scene, "frame_rate", text="Frame Rate")
        layout.prop(scene, "start_frame", text="Start Frame")
        layout.prop(scene, "non_blended_frames", text="Non-Blended Frames")
        layout.prop(scene, "blended_frames", text="Blended Frames")
        layout.prop(scene, "blank_frames", text="Blank Freames")
        layout.prop(scene, "reverse", text="Reverse")
        
        # Opacity Blend Out/In
        layout.separator()
        layout.prop(scene, "opacity_blend_toggle", text="Opacity Blend Out/In")
        
        # Spin Direction
        layout.separator()
        spin_toggle = layout.prop(scene, "spin_toggle", text="Spin")
        if scene.spin_toggle:
            layout.prop_search(scene, "spin_object", scene, "objects", text="Spin Object")
            layout.label(text="Spin Direction:")
            layout.prop(scene, "spin_direction", text="")
        
        # Settings
        layout.separator()
        layout.label(text="Frame Resolution:")
        layout.prop(scene, "frame_resolution", text="")
        layout.label(text="Down Resolution:")
        layout.prop(scene, "down_resolution", text="")
        final_resolution = calculate_final_resolution(scene.down_resolution, total_frames, scene.square_sprite_sheet)
        layout.label(text=f"Final Resolution: {final_resolution[0]} x {final_resolution[1]}")
        layout.separator()
        layout.prop(scene, "square_sprite_sheet", text="Square Sprite Sheet")
        layout.prop(scene, "opacity_clipping", text="Opacity Clipping")
        layout.prop(scene, "filter_nearest", text="Filter Nearest")
        layout.prop(scene, "keep_frames_as_images", text="Keep Frames as Images")
                
        # Bake buttons
        layout.separator()
        layout.operator("object.bake_all", text="Bake")

        # Calculate the final resolution and display it
        layout.separator()
        
        # Directory Selector
        layout.separator()
        layout.label(text="(Required) Save Location:")
        layout.prop(scene, "image_directory", text="")
        layout.label(text="Image Type:")
        layout.prop(scene, "frame_images_type", text="")

        # Create Sprite Sheet button
        layout.separator()
        layout.operator("object.create_sprite_sheet", text="Create Sprite Sheet")

def register():
    bpy.utils.register_class(CreateSpriteSheetOperator)
    bpy.utils.register_class(SetUpSceneOperator)
    bpy.utils.register_class(SpriteShoppePanel)
    bpy.utils.register_class(ReverseOperator)
    bpy.utils.register_class(TemplatesOperator)
    bpy.utils.register_class(BakeAllOperator)

    # Register new properties here
    bpy.types.Scene.reverse = bpy.props.BoolProperty(name="Reverse", default=False)
    bpy.types.Scene.image_directory = bpy.props.StringProperty(name="(Required) Save Location", default="", subtype='DIR_PATH')
    bpy.types.Scene.frame_resolution = bpy.props.IntVectorProperty(
    name="Frame Resolution",
    size=2,
    default=(1024, 1024),
    update=update_resolution
    )
    bpy.types.Scene.down_resolution = bpy.props.IntVectorProperty(name="Down Resolution", size=2, default=(64, 64))
    bpy.types.Scene.filter_nearest = bpy.props.BoolProperty(name="Filter Nearest", default=True)
    bpy.types.Scene.square_sprite_sheet = bpy.props.BoolProperty(name="Square Sprite Sheet")
    bpy.types.Scene.opacity_clipping = bpy.props.BoolProperty(name="Opacity clipping")
    bpy.types.Scene.keep_frames_as_images = bpy.props.BoolProperty(name="Keep Frames as Images")
    bpy.types.Scene.frame_images_type = bpy.props.EnumProperty(
        name="Frame Images Type",
        items=[('PNG', "PNG", "PNG"),
               ('JPEG', "JPEG", "JPEG"),
               ('EXR', "EXR", "EXR"),
               # Add more image file types here if needed
              ],
    )
    bpy.types.Scene.spin_toggle = bpy.props.BoolProperty(name="Spin", default=True)
    bpy.types.Scene.spin_direction = bpy.props.FloatVectorProperty(name="Spin Direction", size=3, subtype='EULER')
    bpy.types.Scene.spin_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.start_frame = bpy.props.IntProperty(
        name="Start Frame",
        default=1,
        min=1,
        
        description="Start frame for the animation"
    )

    bpy.types.Scene.non_blended_frames = bpy.props.IntProperty(
        name="Non-Blended Frames",
        default=12,
        min=0,
        max=128,
        description="Number of non-blended frames"
    )

    bpy.types.Scene.blended_frames = bpy.props.IntProperty(
        name="Blended Frames",
        default=4,
        min=0,
        max=128,
        description="Number of blended frames"
    )

    bpy.types.Scene.blank_frames = bpy.props.IntProperty(
        name="Blank Frames",
        default=0,
        min=0,
        max=128,
        description="Number of blank frames"
    )

    bpy.types.Scene.frame_rate = bpy.props.IntProperty(
        name="Frame Rate",
        default=0,
        min=1,
        max=240,
        description="Animation frame rate",
        update=set_custom_frame_rate
    )

    bpy.types.Scene.opacity_blend_toggle = bpy.props.BoolProperty(
        name="Opacity Blend Out/In",
        default=False,
        description="Toggle opacity blend out/in"
    )
    # Add other properties as needed

   
    
if __name__ == "__main__":
    register()
    
