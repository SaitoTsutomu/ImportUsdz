import os.path
import shutil
import zipfile
from pathlib import Path

import bpy
from bpy.props import FloatProperty

from .register_class import _get_cls

try:
    from more_itertools import first, last
except ModuleNotFoundError as e:
    print(f"{Path(__file__).parent.name}: {e}")


class CIU_OT_import_usdz(bpy.types.Operator):
    """Import Usdz file"""

    bl_idname = "object.import_usdz"
    bl_label = "Import Usdz"
    bl_description = "Import Usdz file."
    bl_options = {"REGISTER", "UNDO"}

    scale: FloatProperty() = FloatProperty(default=1)  # type: ignore

    def execute(self, context):
        # Downloadsの最新usdzファイルを取得
        gl = Path(os.path.expanduser("~/Downloads")).glob("*.usdz")
        file = last(sorted((fnam.stat().st_mtime, fnam) for fnam in gl), (0, ""))[-1]
        if not file:
            self.report({"INFO"}, "No files.")
            return {"CANCELLED"}
        tmpdir = "/tmp/impusdz"
        if os.path.isdir(tmpdir):
            shutil.rmtree(tmpdir)
        os.makedirs(tmpdir, exist_ok=True)
        # tmpdirに解凍
        with zipfile.ZipFile(file) as zf:
            zf.extractall(tmpdir)
        usdc = first(Path(tmpdir).glob("*.usdc"), "")
        if not usdc:
            self.report({"INFO"}, "No usdc.")
            return {"CANCELLED"}
        # usdcをインポート
        scale = self.scale * 0.01
        bpy.ops.wm.usd_import(filepath=str(usdc), scale=scale, import_usd_preview=True)
        # 画像をパック
        bpy.ops.file.pack_all()
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
