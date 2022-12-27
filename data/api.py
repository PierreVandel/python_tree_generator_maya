"""
TREE GENERATOR
Auteur : Pierre Vandel
02/11/2022
PEP8 approved
"""

import random

import maya.OpenMaya as openMaya
import maya.cmds as mc

'''Constants'''
LEAF_COLOR: tuple = (0.23, 0.13, 0.05)
TRUNK_COLOR: tuple = (0.12, 0.4, 0.12)


def generate_trees(number_tree: int,
                   number_ramification: int,
                   is_snap: bool,
                   min_position: float,
                   max_position: float,
                   ground_name: str):
    """
    Function allowing a random stylized tree generation
    :param number_tree: integer
    :param number_ramification: integer
    :param is_snap: boolean
    :param min_position: float
    :param max_position: float
    :param ground_name: string, name for the snapping (optional)
    """
    clean_trees()

    print("Generation...")

    tree_grp = mc.createNode('transform', name='tree_grp')

    for index in range(0, number_tree):
        trunk_transform, trunk_shape, trunk_list_poly_extrude_faces = \
            generate_trunk()
        trunk_transform = mc.rename(trunk_transform, f"trunk{index}")

        '''trunk leaf generation'''
        leaf_transform = generate_leaf(trunk_list_poly_extrude_faces,
                                       trunk_transform)
        mc.rename(leaf_transform, f"leaf{index}")

        mc.parent(trunk_transform, tree_grp)

        '''Branches generation'''
        generate_recursive_branch(index,
                                  trunk_transform,
                                  trunk_list_poly_extrude_faces,
                                  7,
                                  number_ramification)

        '''Set random position tree'''
        set_position(trunk_transform, min_position, max_position)

        '''Snap tree to the closet ground point in Y axis if the given name 
        exists'''
        if is_snap:
            if not mc.ls(f"{ground_name}"):
                mc.warning(f"The node called {ground_name} does not exist")
                return
            snap_to_surface(trunk_transform, ground_name)
    print("Generation succeeded !")


def generate_recursive_branch(index: int,
                              parent_transform,
                              parent_list_poly_extrude_faces: list,
                              level: int,
                              ramification: int):
    """
    Recursive function to generate randoms branches
    :param index: integer for naming
    :param parent_transform: trunk or previous branch
    :param parent_list_poly_extrude_faces: list of all previous branch extrudes
    :param level: integer, extrude number
    :param ramification: integer, branching level
    """

    if ramification == 0:
        return
    ramification -= 1

    while level > 0:
        branch_transform, branch_shape, branch_list_poly_extrude_faces = \
            generate_trunk()
        mc.parent(branch_transform, parent_transform)

        '''leaves generation'''
        leaf_transform = generate_leaf(branch_list_poly_extrude_faces,
                                       branch_transform)
        mc.rename(leaf_transform, f"leaf{index}")

        '''Set random position and rotation branches'''
        mc.setAttr(f"{branch_transform}.translate",
                   parent_list_poly_extrude_faces[level][0],
                   parent_list_poly_extrude_faces[level][1],
                   parent_list_poly_extrude_faces[level][2])
        mc.setAttr(f"{branch_transform}.rotateY", random.uniform(-180, 180))
        mc.setAttr(f"{branch_transform}.rotateX", random.uniform(40, 70))

        '''For each level of branches, the scale is decreases, may be a 
        parameter later'''
        scale: float = 0.6
        mc.setAttr(f"{branch_transform}.scale", scale, scale, scale)

        '''recursion'''
        generate_recursive_branch(index,
                                  branch_transform,
                                  branch_list_poly_extrude_faces,
                                  level,
                                  ramification)
        level -= 1


def generate_trunk():
    """
    Function allowing branches and trunk generation
    :return: tree_transform, tree_shape, list_poly_extrude_faces
    """
    trunk_radius_start: int = 1
    trunk_horizontal_subdivision: int = 15
    trunk_size: int = int(random.uniform(8, 12))

    tree = mc.polyDisc(
        r=trunk_radius_start,
        s=trunk_horizontal_subdivision,
        sd=1,
        sm=1
    )
    mc.polyColorPerVertex(rgb=LEAF_COLOR, cdo=True)
    tree_transform = tree[0]

    mc.select(f'{tree_transform}.f[*]')

    list_poly_extrude_faces = list()
    for i in range(0, trunk_size):
        random_rotation: float = random.uniform(-5, 5)
        random_scale: float = random.uniform(0.5, 0.9)
        random_translate_z: float = random.uniform(0.7, 0.9)

        poly_extrude_face = mc.polyExtrudeFacet()[0]
        mc.setAttr(f"{poly_extrude_face}.localTranslate", 0, 0,
                   random_translate_z)
        mc.setAttr(f"{poly_extrude_face}.rotate", random_rotation, 0,
                   random_rotation)
        mc.setAttr(f"{poly_extrude_face}.localScale", random_scale,
                   random_scale, random_scale)

        list_poly_extrude_faces.append((
            mc.getAttr(f"{poly_extrude_face}.pivotX"),
            mc.getAttr(f"{poly_extrude_face}.pivotY"),
            mc.getAttr(f"{poly_extrude_face}.pivotZ")
        ))

    tree_shape = tree[1]
    return tree_transform, tree_shape, list_poly_extrude_faces


def generate_leaf(list_poly_extrude_faces: list, parent: str):
    """
    Function for leaf generation
    :param list_poly_extrude_faces: list
    :param parent: string, parent branch name transform
    :return:
    """
    leaf_transform = mc.polySphere()[0]
    mc.polyColorPerVertex(rgb=TRUNK_COLOR, cdo=True)
    mc.setAttr(f"{leaf_transform}.translate",
               list_poly_extrude_faces[-1][0],
               list_poly_extrude_faces[-1][1],
               list_poly_extrude_faces[-1][2])
    mc.setAttr(f"{leaf_transform}.scale", 1.5, 1.5, 1.5)
    mc.parent(leaf_transform, parent)
    return leaf_transform


def set_position(transform, min_position: float, max_position: float):
    """
    Function to set the random position tree
    :param transform: tree
    :param min_position: float
    :param max_position: float
    :return:
    """
    mc.setAttr(f"{transform}.translateX", random.uniform(min_position,
                                                         max_position))
    mc.setAttr(f"{transform}.translateZ", random.uniform(min_position,
                                                         max_position))


def ray_intersect(mesh, point: tuple, direction: tuple):
    """
    Function to create a ray cast
    :param mesh: ground
    :param point: start point to the direction vector
    :param direction: direction vector
    :return: intersection between mesh and ray
    """
    mc.select(cl=True)
    openMaya.MGlobal.selectByName(mesh)
    sel_list = openMaya.MSelectionList()
    openMaya.MGlobal.getActiveSelectionList(sel_list)
    item = openMaya.MDagPath()
    sel_list.getDagPath(0, item)
    item.extendToShape()
    fn_mesh = openMaya.MFnMesh(item)
    ray_source = openMaya.MFloatPoint(point[0], point[1], point[2], 1.0)
    ray_dir = openMaya.MFloatVector(direction[0], direction[1], direction[2])
    face_ids = None
    tri_ids = None
    ids_sorted = False
    test_both_directions = False
    max_param = 999999
    world_space = openMaya.MSpace.kWorld
    accel_params = None
    sort_hits = True
    hit_points = openMaya.MFloatPointArray()
    hit_ray_params = openMaya.MFloatArray()
    hit_faces = openMaya.MIntArray()
    hit_tris = None
    hit_bary1 = None
    hit_bary2 = None
    tolerance = 0.0001
    hit = fn_mesh.allIntersections(ray_source, ray_dir, face_ids, tri_ids,
                                   ids_sorted, world_space, max_param,
                                   test_both_directions, accel_params,
                                   sort_hits, hit_points, hit_ray_params,
                                   hit_faces, hit_tris, hit_bary1, hit_bary2,
                                   tolerance)

    return hit, hit_points, hit_faces


def snap_to_surface(mesh, ground):
    """
    Function allows snapping to a mesh
    :param mesh: tree
    :param ground: mesh used for the tree snapping
    :return: nothing
    """
    ground_transform = mc.ls(ground)[0]
    if not ground_transform:
        print("The ground doesn't exist")
        return

    hit, hit_points, hit_faces = ray_intersect(ground_transform, (
        mc.getAttr(f"{mesh}.translateX"),
        mc.getAttr(f"{mesh}.translateY"),
        mc.getAttr(f"{mesh}.translateZ")), (0, -1, 0))

    if not hit:
        hit, hit_points, hit_faces = ray_intersect(ground_transform, (
            mc.getAttr(f"{mesh}.translateX"),
            mc.getAttr(f"{mesh}.translateY"),
            mc.getAttr(f"{mesh}.translateZ")), (0, 1, 0))

        if not hit:
            mc.warning("There are no ground below and on the tree")
            return

    mc.setAttr(f"{mesh}.translateY", hit_points[0].y)


def clean_trees():
    """
    Delete all trees in the scene
    :return:
    """
    tree_grp = mc.ls("tree_grp*")
    if tree_grp:
        mc.delete(tree_grp)
