import bpy
from mathutils import Vector


def track_camera_to_flock(cam_obj, flock, frame):
    """
    Point the camera at the flock's current centroid.
    Calculates direction vector and sets camera rotation, then keyframes it.
    """
    centroid = flock.centroid
    cam_loc  = Vector(cam_obj.location)
    direction = centroid - cam_loc

    # align camera -Z to direction, Y up
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=frame)
