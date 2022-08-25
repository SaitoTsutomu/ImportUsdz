import bpy
from bpy.props import FloatProperty

from .register_class import _get_cls


class CIU_OT_import_usdz(bpy.types.Operator):
    """Import Usdz file"""

    bl_idname = "object.import_usdz"
    bl_label = "Import Usdz"
    bl_description = "Import Usdz file."
    bl_options = {"REGISTER", "UNDO"}

    scale: FloatProperty() = FloatProperty(default=1)  # type: ignore

    def execute(self, context):

        return {"FINISHED"}


class CIU_PT_bit(bpy.types.Panel):
    bl_label = "ImportUsdz"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"

    def draw(self, context):
        self.layout.prop(context.scene, "scale", text="Scale")
        text = CIU_OT_import_usdz.bl_label
        prop = self.layout.operator(CIU_OT_import_usdz.bl_idname, text=text)
        prop.scale = context.scene.scale


# __init__.pyで使用
ui_classes = _get_cls(__name__)
