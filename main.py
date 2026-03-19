import bpy
import os
import sys
import importlib

# ── path bootstrap ────────────────────────────────────────────────────────────
_dir = os.path.dirname(bpy.context.space_data.text.filepath)
print(f"[metaflock] root: {_dir}")
if _dir not in sys.path:
    sys.path.append(_dir)

# ── reload all modules (dev loop) ────────────────────────────────────────────
import scene
import materials
import metaballs
import flock
import camera
import behaviors
import behaviors.boids
import behaviors.lavalamp

for mod in (scene, materials, metaballs, flock, camera, behaviors, behaviors.boids, behaviors.lavalamp):
    importlib.reload(mod)

# ── local imports ─────────────────────────────────────────────────────────────
from scene import clear_scene, setup_camera, setup_light, setup_render_settings
from materials import create_flat_green_material, apply_material
from metaballs import create_metaball_object, add_metaball_element, sync_metaballs_to_flock, keyframe_flock
from flock import init_flock, step_flock
from camera import track_camera_to_flock
from behaviors.boids import BoidsBehavior
from behaviors.lavalamp import LavaLampBehavior

# ── config ────────────────────────────────────────────────────────────────────
N_AGENTS     = 12
FRAME_START  = 1
FRAME_END    = 120
FPS          = 24

CAM_LOCATION = (10, -10, 6)
LIGHT_LOC    = (5, 5, 10)
LIGHT_ENERGY = 800


def run(behavior=None):
    if behavior is None:
        behavior = BoidsBehavior()

    # scene
    clear_scene()
    cam = setup_camera(CAM_LOCATION)
    setup_light("POINT", LIGHT_LOC, LIGHT_ENERGY)
    setup_render_settings(FPS, FRAME_START, FRAME_END)

    # metaballs
    mb_obj, mb_data = create_metaball_object("MetaFlock")
    mat = create_flat_green_material()
    apply_material(mb_obj, mat)

    # flock
    fl = init_flock(N_AGENTS, behavior)

    # seed metaball elements — one per agent
    for agent in fl.agents:
        add_metaball_element(mb_data, agent.position, agent.radius, agent.stiffness)

    # bake
    bake_animation(cam, mb_obj, mb_data, fl, FRAME_START, FRAME_END)

    print("[metaflock] done.")


def bake_animation(cam, mb_obj, mb_data, fl, frame_start, frame_end):
    scene_ref = bpy.context.scene
    for frame in range(frame_start, frame_end + 1):
        scene_ref.frame_set(frame)
        step_flock(fl)
        sync_metaballs_to_flock(mb_data, fl)
        keyframe_flock(mb_data, fl, frame)
        track_camera_to_flock(cam, fl, frame)

    scene_ref.frame_set(frame_start)


# ── run ───────────────────────────────────────────────────────────────────────
run()
