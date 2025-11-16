Pack Box
========

Pack objects into a box using both arms.

.. image:: ../_static/imgs/pack_box.png
   :alt: Pack Box Task
   :align: center
   :width: 60%

.. code-block:: python

    from roboeval.envs.pack_objects import (
        PackBox,
        PackBoxPosition,
        PackBoxOrientation,
        PackBoxPositionAndOrientation
    )

**Variations:** 4

Task Description
----------------

Close the flaps of an open packing box using both robot arms. The box has two flaps that must be closed to achieve success.

Success Criteria
----------------

- Both box flaps closed (joint states close to 0, within 0.1 tolerance)

**Task Stages:**

1. Stage 1: Left gripper grasping left flap
2. Stage 2: Right gripper grasping right flap
3. Stage 3: Right flap closed
4. Stage 4: Left flap closed
5. Stage 5: Both flaps fully closed

Key Skills
----------

- Multi-object manipulation
- Spatial planning
- Efficient packing
- Gentle placement
