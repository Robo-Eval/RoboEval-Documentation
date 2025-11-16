Manipulation Tasks
==================

Basic bimanual manipulation primitives.

StackTwoBlocks
--------------

Stack one cube on top of another using bimanual coordination.

.. image:: ../_static/imgs/stack_two_blocks.png
   :alt: Stack Two Blocks Task
   :align: center
   :width: 60%

.. code-block:: python

    from roboeval.envs.manipulation import (
        StackTwoBlocks,
        StackTwoBlocksPosition,
        StackTwoBlocksOrientation,
        StackTwoBlocksPositionAndOrientation
    )

**Variations:** 4

**Task Description:**

The robot must stack two blocks on top of each other. The bottom block must remain on the table, and the top block must be placed on the bottom block.

**Success Criteria:**

- Bottom block is colliding with the table
- Top block is colliding with the bottom block
- Top block is NOT colliding with the table
- Neither gripper is holding either block

**Task Stages:**

1. Stage 1: Grasping one of the blocks
2. Stage 2: Grasping the other block
3. Stage 3: Blocks successfully stacked

CubeHandover
------------

Transfer a cube (rod-shaped object) from one gripper to the other.

.. image:: ../_static/imgs/cube_handover.png
   :alt: Cube Handover Task
   :align: center
   :width: 60%

.. code-block:: python

    from roboeval.envs.manipulation import (
        CubeHandover,
        CubeHandoverPosition,
        CubeHandoverOrientation,
        CubeHandoverPositionAndOrientation,
        VerticalCubeHandover
    )

**Variations:** 5 (including VerticalCubeHandover)

**Task Description:**

The robot must grasp a cube with one gripper, then transfer it to the other gripper. The task tracks which gripper initially holds the object and requires successful transfer to the opposite hand.

**Success Criteria:**

- Cube initially grasped by one gripper (left or right)
- Cube successfully transferred to the opposite gripper
- Initial gripper no longer holding the cube

**VerticalCubeHandover:**

A variant where the cube is oriented vertically (rotated 90°) during the handover, requiring different grasping strategies and maintaining vertical orientation.

**Task Stages:**

1. Stage 1: Cube grasped by initial gripper
2. Stage 2: Cube successfully transferred to opposite gripper

Key Skills
----------

- Basic grasping
- Bimanual coordination
- Object transfer
- Spatial precision
