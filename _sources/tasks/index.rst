Tasks Overview
==============

RoboEval includes **8 task families** with **28 total variations** designed to test different aspects of bimanual manipulation.

Task Families
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Task Family
     - Variations
     - Description
   * - :doc:`lift-pot`
     - 4
     - Grasp pot by handles and lift without tilting
   * - :doc:`stack-books`
     - 3
     - Stack books on shelves requiring precise placement
   * - :doc:`stack-books`
     - 4
     - Pick books from table and transfer between hands
   * - :doc:`manipulation`
     - 4
     - Stack blocks requiring bimanual coordination
   * - :doc:`manipulation`
     - 5
     - Transfer cube between robot hands (includes vertical handover)
   * - :doc:`rotate-valve`
     - 3
     - Rotate valve wheel with continuous bimanual coordination
   * - :doc:`pack-box`
     - 4
     - Pack objects into a box requiring spatial reasoning
   * - :doc:`lift-tray`
     - 5
     - Lift tray with objects maintaining balance (includes drag-over variant)

Variation Types
---------------

Most tasks have 4 standard variations:

**Base** - Static configuration
    Objects appear in same position every episode

**Position** - Positional randomization
    Object positions randomized within workspace

**Orientation** - Rotational randomization  
    Object orientations randomized (typically ±30° around Z-axis)

**Position and Orientation** - Full randomization
    Both position and orientation randomized

Quick Reference
---------------

.. code-block:: python

    # Lift Pot (4 variations)
    from roboeval.envs.lift_pot import (
        LiftPot, LiftPotPosition, 
        LiftPotOrientation, LiftPotPositionAndOrientation
    )
    
    # Stack Single Book Shelf (3 variations)
    from roboeval.envs.stack_books import (
        StackSingleBookShelf, StackSingleBookShelfPosition,
        StackSingleBookShelfPositionAndOrientation
    )
    
    # Pick Single Book From Table (4 variations)
    from roboeval.envs.stack_books import (
        PickSingleBookFromTable, PickSingleBookFromTablePosition,
        PickSingleBookFromTableOrientation, PickSingleBookFromTablePositionAndOrientation
    )
    
    # Stack Two Blocks (4 variations)
    from roboeval.envs.manipulation import (
        StackTwoBlocks, StackTwoBlocksPosition,
        StackTwoBlocksOrientation, StackTwoBlocksPositionAndOrientation
    )
    
    # Cube Handover (5 variations)
    from roboeval.envs.manipulation import (
        CubeHandover, CubeHandoverPosition, CubeHandoverOrientation,
        CubeHandoverPositionAndOrientation, VerticalCubeHandover
    )
    
    # Rotate Valve (3 variations)
    from roboeval.envs.rotate_utility_objects import (
        RotateValve, RotateValvePosition, RotateValvePositionAndOrientation
    )
    
    # Pack Box (4 variations)
    from roboeval.envs.pack_objects import (
        PackBox, PackBoxPosition, PackBoxOrientation, PackBoxPositionAndOrientation
    )
    
    # Lift Tray (5 variations)
    from roboeval.envs.lift_tray import (
        LiftTray, LiftTrayPosition, LiftTrayOrientation,
        LiftTrayPositionAndOrientation, DragOverAndLiftTray
    )

Task Progression Stages
------------------------

Each task defines progression stages for fine-grained evaluation:

**Example: LiftPot**

- Stage 0: Initial state
- Stage 1: Left gripper grasping pot
- Stage 2: Right gripper grasping pot
- Stage 3: Pot lifted 0.1m above table
- Stage 4: Success (pot stable and level)

Access stages during execution:

.. code-block:: python

    obs, reward, terminated, truncated, info = env.step(action)
    current_stage = info['metrics']['stage']

Metrics
-------

All tasks provide rich metrics:

- **Success rate** - Binary task completion
- **Task progression** - Furthest stage reached
- **Coordination quality** - Bimanual synchronization
- **Trajectory efficiency** - Path length and smoothness
- **Safety** - Collision avoidance

See :doc:`../advanced/metrics` for details.

Choosing a Task
---------------

**For Learning Bimanual Coordination:**

- ``StackTwoBlocks`` - Basic block stacking
- ``LiftPot`` - Coordinated lifting
- ``LiftTray`` - Balance and coordination

**For Precision and Placement:**

- ``PickSingleBookFromTable`` - Precise grasping and placement
- ``StackSingleBookShelf`` - Shelf alignment
- ``PackBox`` - Spatial reasoning

**For Continuous Coordination:**

- ``RotateValve`` - Continuous bimanual motion
- ``DragOverAndLiftTray`` - Complex multi-stage manipulation

**For Hand-to-Hand Transfer:**

- ``CubeHandover`` - Horizontal transfer
- ``VerticalCubeHandover`` - Vertical transfer

**For Testing Generalization:**

- Use ``Position`` variations for position robustness
- Use ``Orientation`` variations for rotation robustness
- Use ``PositionAndOrientation`` for full randomization

Task Details
------------

.. toctree::
   :maxdepth: 1

   lift-pot
   stack-books
   manipulation
   rotate-valve
   pack-box
   lift-tray
