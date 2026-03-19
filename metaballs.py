import bpy
from mathutils import Vector


def create_metaball_object(name="MetaFlock", threshold=0.6, resolution=0.3):
    """
    Create a MetaBall datablock and its parent object.
    Returns (object, metaball_data).
    """
    mb_data = bpy.data.metaballs.new(name)
    mb_data.threshold  = threshold
    mb_data.resolution = resolution

    mb_obj = bpy.data.objects.new(name, mb_data)
    bpy.context.scene.collection.objects.link(mb_obj)

    print(f"[metaballs] '{name}' created — threshold={threshold}, resolution={resolution}")
    return mb_obj, mb_data


def add_metaball_element(mb_data, location=(0, 0, 0), radius=1.0, stiffness=1.0):
    """Add a single MetaElement to an existing metaball datablock."""
    el           = mb_data.elements.new()
    el.co        = Vector(location)
    el.radius    = radius
    el.stiffness = stiffness
    return el


def sync_metaballs_to_flock(mb_data, flock):
    """
    Write current agent positions, radius, and stiffness
    into metaball elements. Assumes elements and agents are same length.
    """
    for el, agent in zip(mb_data.elements, flock.agents):
        el.co        = Vector(agent.position)
        el.radius    = agent.radius
        el.stiffness = agent.stiffness


def keyframe_flock(mb_data, flock, frame):
    """Insert keyframes on position, radius, and stiffness for all elements."""
    for el in mb_data.elements:
        el.keyframe_insert(data_path="co",        frame=frame)
        el.keyframe_insert(data_path="radius",    frame=frame)
        el.keyframe_insert(data_path="stiffness", frame=frame)
