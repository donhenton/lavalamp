from mathutils import Vector


# ── tuning ────────────────────────────────────────────────────────────────────
NEIGHBOR_RADIUS   = 3.0
SEPARATION_RADIUS = 1.2
MAX_SPEED         = 0.15

W_SEPARATION = 1.8
W_ALIGNMENT  = 1.0
W_COHESION   = 1.0


class BoidsBehavior:
    """
    Classic Reynolds boids — separation, alignment, cohesion.
    Swap this out by passing a different behavior to init_flock().
    Any behavior must implement: step(flock) -> None
    """

    def step(self, flock):
        agents = flock.agents
        new_velocities = []

        for agent in agents:
            neighbors = [
                a for a in agents
                if a is not agent and (a.position - agent.position).length < NEIGHBOR_RADIUS
            ]

            separation = self._separation(agent, neighbors)
            alignment  = self._alignment(agent, neighbors)
            cohesion   = self._cohesion(agent, neighbors)

            vel = (
                agent.velocity
                + separation * W_SEPARATION
                + alignment  * W_ALIGNMENT
                + cohesion   * W_COHESION
            )

            # clamp speed
            if vel.length > MAX_SPEED:
                vel = vel.normalized() * MAX_SPEED

            new_velocities.append(vel)

        for agent, vel in zip(agents, new_velocities):
            agent.velocity  = vel
            agent.position += vel

    # ── rules ─────────────────────────────────────────────────────────────────

    def _separation(self, agent, neighbors):
        steer = Vector((0, 0, 0))
        close = [n for n in neighbors if (n.position - agent.position).length < SEPARATION_RADIUS]
        for n in close:
            diff = agent.position - n.position
            if diff.length > 0:
                steer += diff.normalized() / diff.length
        return steer

    def _alignment(self, agent, neighbors):
        if not neighbors:
            return Vector((0, 0, 0))
        avg_vel = Vector((0, 0, 0))
        for n in neighbors:
            avg_vel += n.velocity
        avg_vel /= len(neighbors)
        return (avg_vel - agent.velocity) * 0.1

    def _cohesion(self, agent, neighbors):
        if not neighbors:
            return Vector((0, 0, 0))
        center = Vector((0, 0, 0))
        for n in neighbors:
            center += n.position
        center /= len(neighbors)
        return (center - agent.position) * 0.01
