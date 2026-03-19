import math
import random
from mathutils import Vector


# ── tuning ────────────────────────────────────────────────────────────────────
RISE_SPEED      = 0.015   # max vertical speed
DRIFT_SPEED     = 0.003   # random horizontal wander
WALL_PULL       = 0.02    # strength of center-pull on X/Y (lamp walls)
WALL_RADIUS     = 2.5     # how far from center before wall pull kicks in
VERTICAL_RANGE  = 3.0     # half-height of the lamp column


class LavaLampBehavior:
    """
    Lava lamp simulation — agents rise and fall independently on phase-offset
    sine waves, constrained to a vertical column, oblivious to each other.
    The metaball field handles all visual merging naturally.

    Signature matches BoidsBehavior: step(flock) -> None
    Requires agents to have a .phase attribute — injected at first step if missing.
    """

    def __init__(self, speed=RISE_SPEED):
        self.speed = speed
        self.frame = 0

    def step(self, flock):
        self.frame += 1

        for agent in flock.agents:
            # inject phase on first encounter
            if not hasattr(agent, 'phase'):
                agent.phase = random.uniform(0, 2 * math.pi)

            # vertical oscillation driven by sine + phase offset
            vertical = math.sin(self.frame * 0.04 + agent.phase) * self.speed

            # subtle random horizontal drift
            drift_x = random.uniform(-DRIFT_SPEED, DRIFT_SPEED)
            drift_y = random.uniform(-DRIFT_SPEED, DRIFT_SPEED)

            # wall pull — nudge back toward center if too far out
            wall_x = -agent.position.x * WALL_PULL if abs(agent.position.x) > WALL_RADIUS else 0
            wall_y = -agent.position.y * WALL_PULL if abs(agent.position.y) > WALL_RADIUS else 0

            agent.velocity = Vector((
                drift_x + wall_x,
                drift_y + wall_y,
                vertical,
            ))

            agent.position += agent.velocity

            # soft clamp vertical range
            if agent.position.z > VERTICAL_RANGE:
                agent.position.z = VERTICAL_RANGE
            elif agent.position.z < -VERTICAL_RANGE:
                agent.position.z = -VERTICAL_RANGE
