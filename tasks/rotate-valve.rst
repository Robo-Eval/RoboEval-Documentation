Rotate Valve
============

Rotate a valve wheel using bimanual coordination.

.. image:: ../_static/imgs/rotate_valve.png
   :alt: Rotate Valve Task
   :align: center
   :width: 60%

.. code-block:: python

    from roboeval.envs.rotate_utility_objects import (
        RotateValve,
        RotateValvePosition,
        RotateValvePositionAndOrientation
    )

**Variations:** 3

Task Description
----------------

Rotate two valve wheels through coordinated bimanual manipulation. Each valve must be rotated at least 0.10 radians (approximately 5.7 degrees) from its initial position.

Success Criteria
----------------

- Both valves rotated ≥ 0.10 radians from initial state
- Valves not colliding with floor

**Task Stages:**

1. Stage 1: Grasping first valve
2. Stage 2: First valve rotated ≥ 0.10 radians
3. Stage 3: Grasping second valve
4. Stage 4: Second valve rotated ≥ 0.10 radians

Key Skills
----------

- Continuous bimanual coordination
- Regrasping strategies
- Force control
- Synchronized movement
