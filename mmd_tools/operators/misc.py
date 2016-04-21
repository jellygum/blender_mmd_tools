# -*- coding: utf-8 -*-

import bpy
from bpy.types import Operator

from mmd_tools import utils
from mmd_tools.core import model as mmd_model


class SeparateByMaterials(Operator):
    bl_idname = 'mmd_tools.separate_by_materials'
    bl_label = 'Separate by materials'
    bl_description = 'Separate by materials'
    bl_options = {'PRESET'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        root = mmd_model.Model.findRoot(obj)
        if root and root.mmd_root.editing_morph:            
            self.report({ 'ERROR' }, "You are editing a morph, apply or clear it before proceed")
            return { 'CANCELLED' }
        utils.separateByMaterials(obj)
        if root and len(root.mmd_root.material_morphs) > 0:
            pass  # TODO: we need to update the references to the mesh object on the material morph offsets
        utils.clearUnusedMeshes()
        return {'FINISHED'}

class JoinMeshes(Operator):
    bl_idname = 'mmd_tool.join_meshes'
    bl_label = 'Join Meshes'
    bl_description = 'Join the Model meshes into a single one'
    bl_options = {'PRESET'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        root = mmd_model.Model.findRoot(obj)
        if root is None:
            self.report({ 'ERROR' }, 'Select a MMD model') 
            return { 'CANCELLED' } 

        if root.mmd_root.editing_morph:            
            self.report({ 'ERROR' }, "You are editing a morph, apply or clear it before proceed")
            return { 'CANCELLED' }
        # Find all the meshes in mmd_root and join them          
        rig = mmd_model.Model(root)
        bpy.ops.object.select_all(action='DESELECT')
        for mesh in rig.meshes():
            mesh.select = True
        bpy.context.scene.objects.active = rig.firstMesh()        
        bpy.ops.object.join()
        if len(root.mmd_root.material_morphs) > 0:
            pass  # TODO: update the mesh references

        utils.clearUnusedMeshes()
        return { 'FINISHED' }
        