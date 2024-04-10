bl_info = {
    "name": "Create Bendy Segment",
    "author": "Velaguez Szpiech",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "description": "Creates a path with evenly distributed controls",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Armature"}
    
import bpy


class AlongACurvePanel(bpy.types.Panel):
    bl_label = "Path Segments"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Rigging"
        
    def draw(self, context):
        
        layout = self. layout        
        scn = context.scene
        col = layout.column(align=True)
        row = layout.row()
        
        col.prop(scn, "ObjectsAlongPath_Count")
        col.prop(scn, "ObjectAlongPath_curveName")               
                    
        self.layout.operator("armature.create_along_a_path")


class CreateObjectsAlongACurve(bpy.types.Operator):
    """Creates a path with evenly distributed objects along it"""
    bl_idname = "armature.create_along_a_path"
    bl_label = "Create Objects Along A Path"
    bl_options = {'REGISTER', 'UNDO'}
    
    def MakeSimpleControlObj(self, controlName='cr_simpleMarker'):
        bpy.ops.mesh.primitive_circle_add(radius=0.25, vertices=8, view_align=False, enter_editmode=True, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.mesh.primitive_circle_add(radius=0.25, vertices=8, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))   
        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.mesh.primitive_circle_add(radius=0.25, vertices=8, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)    
        bpy.ops.object.editmode_toggle()
        bpy.context.active_object.name = controlName;
            
        return bpy.data.objects[controlName]

    def makeSpline(self, objName, coords, location):
        #Creates a spline with the provided list of Vector coordinates
        curveName = objName + '_curve'
        #create curve data block
        curveData = bpy.data.curves.new(curveName, type='CURVE')
        curveData.dimensions = '3D'
        curveData.resolution_u = 6

        #create the object data block
        objectData = bpy.data.objects.new(objName, curveData)
        objectData.location = location
        
        #create the spline
        line = curveData.splines.new('NURBS')
        line.order_u = 3
        line.use_endpoint_u = True
        line.use_endpoint_v = True
        line.points.add(len(coords)-1)
        
        for i, num in enumerate(coords):
            x,y,z = coords[i]
            line.points[i].co = (x, y, z, 1)
        
        #link it to the scene
        bpy.context.scene.objects.link(objectData)
        objectData.select = True
        
        return objectData     


    def execute(self, context):    
        name = bpy.data.scenes['Scene'].ObjectAlongPath_curveName                                 
        coords = [(0,0,0), (0,0,5)]
        splineObj = self.makeSpline(name, coords, bpy.context.scene.cursor_location)
        count = bpy.data.scenes['Scene'].ObjectsAlongPath_Count

        for i in range(count):
            control = self.MakeSimpleControlObj('cr_' + name + '_marker_' + str(i))
            bpy.ops.object.constraint_add(type='FOLLOW_PATH')
            bpy.context.object.constraints["Follow Path"].target = bpy.data.objects[splineObj.name]
            bpy.context.object.constraints["Follow Path"].use_fixed_location = True
            bpy.context.object.constraints["Follow Path"].offset_factor = i / (count - 1);

        bpy.ops.object.select_all(action='TOGGLE')
        
        return {'FINISHED'}
    
   

def register():
    bpy.utils.register_class(AlongACurvePanel)
    bpy.utils.register_class(CreateObjectsAlongACurve)
    bpy.types.Scene.ObjectsAlongPath_Count = bpy.props.IntProperty(
                    name="Count",
                    description="Number of Objects distributed along the path",
                    min=1, max = 1000,
                    default=6,                    
                    )
    bpy.types.Scene.ObjectAlongPath_curveName = bpy.props.StringProperty(
                    name="curveName",
                    description="Name given to the object and curve",
                    default="PathObjectSegment",
                    )
    
def unregister():
    bpy.utils.unregister_class(CreateObjectsAlongACurve)
    bpy.utils.unregister_class(AlongACurvePanel)
    del bpy.types.Scene.ObjectsAlongPath_Count
    del bpy.types.Scene.ObjectAlongPath_curveName

if __name__ == "__main__":
    register()