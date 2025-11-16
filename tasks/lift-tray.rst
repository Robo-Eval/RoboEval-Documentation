Lift Tray
=========

Grasp and lift a tray with objects, maintaining balance.

.. image:: ../_static/imgs/lift_tray.png
   :alt: Lift Tray Task
   :align: center
   :width: 60%

.. code-block:: python

    from roboeval.envs.lift_tray import (
        LiftTray,
        LiftTrayPosition,
        LiftTrayOrientation,
        LiftTrayPositionAndOrientation,
        DragOverAndLiftTray
    )

**Variations:** 5

LiftTray Variations
-------------------

Standard lift with randomization variations (4 total).

DragOverAndLiftTray
-------------------

Additional variant: drag tray over an obstacle before lifting.

**Additional constraints:**

- Must drag tray horizontally
- Clear obstacle without tipping
- Then lift to target height

Success Criteria
----------------

- Both grippers holding the tray (both sides)
- Tray NOT colliding with the table
- Tray maintained level

**Task Stages:**

1. Stage 1: Left gripper grasping the tray
2. Stage 2: Right gripper grasping the tray  
3. Stage 3: Tray lifted (both grippers holding, not colliding with table or floor)

Key Skills
----------

- Coordinated lifting
- Balance control
- Force distribution
- Smooth trajectories
