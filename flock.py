import random
from mathutils import Vector


class Agent:
    def __init__(self, position, velocity, radius=0.8, stiffness=1.2):
        self.position  = Vector(position)
        self.velocity  = Vector(velocity)
        self.radius    = radius
        self.stiffness = stiffness


class Flock:
    def __init__(self, agents, behavior):
        self.agents   = agents
        self.behavior = behavior

    @property
    def centroid(self):
        if not self.agents:
            return Vector((0, 0, 0))
        total = Vector((0, 0, 0))
        for a in self.agents:
            total += a.position
        return total / len(self.agents)


def init_flock(n_agents, behavior, spawn_radius=3.0):
    """
    Create n agents with randomized positions and velocities.
    Attach a behavior object — anything with a step(flock) method.
    """
    agents = []
    for _ in range(n_agents):
        pos = Vector((
            random.uniform(-spawn_radius, spawn_radius),
            random.uniform(-spawn_radius, spawn_radius),
            random.uniform(-spawn_radius, spawn_radius),
        ))
        vel = Vector((
            random.uniform(-0.5, 0.5),
            random.uniform(-0.5, 0.5),
            random.uniform(-0.5, 0.5),
        ))
        agents.append(Agent(pos, vel))

    print(f"[flock] initialized {n_agents} agents with {type(behavior).__name__}")
    return Flock(agents, behavior)


def step_flock(flock):
    """Advance the flock one tick by delegating entirely to the behavior."""
    flock.behavior.step(flock)
