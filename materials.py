import bpy


def create_flat_green_material():
    """Create a flat green material with no specular variation."""
    mat = bpy.data.materials.new("FlatGreen")
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output   = nodes.new("ShaderNodeOutputMaterial")
    bsdf     = nodes.new("ShaderNodeBsdfDiffuse")

    bsdf.inputs["Color"].default_value    = (0.05, 0.6, 0.15, 1.0)
    bsdf.inputs["Roughness"].default_value = 1.0

    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

    print("[materials] flat green material created.")
    return mat


def apply_material(obj, material):
    """Apply a material to an object, replacing any existing slots."""
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
    print(f"[materials] applied '{material.name}' to '{obj.name}'")
