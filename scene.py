import bpy


def clear_scene():
    """Remove all objects, meshes, lights, cameras, and metaball data."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)

    for block in list(bpy.data.meshes):
        bpy.data.meshes.remove(block)
    for block in list(bpy.data.metaballs):
        bpy.data.metaballs.remove(block)
    for block in list(bpy.data.cameras):
        bpy.data.cameras.remove(block)
    for block in list(bpy.data.lights):
        bpy.data.lights.remove(block)
    for block in list(bpy.data.materials):
        bpy.data.materials.remove(block)

    print("[scene] cleared.")


def setup_camera(location=(10, -10, 6)):
    """Create a camera at location. Pointing is handled per-frame by camera.py."""
    cam_data = bpy.data.cameras.new("Camera")
    cam_obj  = bpy.data.objects.new("Camera", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = location
    print(f"[scene] camera at {location}")
    return cam_obj


def setup_light(light_type="POINT", location=(5, 5, 10), energy=800):
    """Add a light of given type at location with given energy."""
    light_data = bpy.data.lights.new("Light", type=light_type)
    light_data.energy = energy
    light_obj  = bpy.data.objects.new("Light", light_data)
    bpy.context.scene.collection.objects.link(light_obj)
    light_obj.location = location
    print(f"[scene] {light_type} light at {location}, energy={energy}")
    return light_obj


def setup_render_settings(fps=24, frame_start=1, frame_end=120):
    """Configure FPS, frame range, and resolution."""
    scene = bpy.context.scene
    scene.render.fps          = fps
    scene.frame_start         = frame_start
    scene.frame_end           = frame_end
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    print(f"[scene] render: {fps}fps, frames {frame_start}–{frame_end}")
