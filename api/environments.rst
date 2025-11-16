Environments API
================

Task environment classes.

Lift Pot Environments
---------------------

.. code-block:: python

    from roboeval.envs.lift_pot import (
        LiftPot,
        LiftPotPosition,
        LiftPotOrientation,
        LiftPotPositionAndOrientation
    )

Stack Books Environments
------------------------

.. code-block:: python

    from roboeval.envs.stack_books import (
        StackSingleBookShelf,
        StackSingleBookShelfPosition,
        StackSingleBookShelfPositionAndOrientation,
        PickSingleBookFromTable,
        PickSingleBookFromTablePosition,
        PickSingleBookFromTableOrientation,
        PickSingleBookFromTablePositionAndOrientation
    )

Manipulation Environments
-------------------------

.. code-block:: python

    from roboeval.envs.manipulation import (
        StackTwoBlocks,
        StackTwoBlocksPosition,
        StackTwoBlocksOrientation,
        StackTwoBlocksPositionAndOrientation,
        CubeHandover,
        CubeHandoverPosition,
        CubeHandoverOrientation,
        CubeHandoverPositionAndOrientation,
        VerticalCubeHandover
    )

Rotate Valve Environments
-------------------------

.. code-block:: python

    from roboeval.envs.rotate_utility_objects import (
        RotateValve,
        RotateValvePosition,
        RotateValvePositionAndOrientation
    )

Pack Box Environments
---------------------

.. code-block:: python

    from roboeval.envs.pack_objects import (
        PackBox,
        PackBoxPosition,
        PackBoxOrientation,
        PackBoxPositionAndOrientation
    )

Lift Tray Environments
----------------------

.. code-block:: python

    from roboeval.envs.lift_tray import (
        LiftTray,
        LiftTrayPosition,
        LiftTrayOrientation,
        LiftTrayPositionAndOrientation,
        DragOverAndLiftTray
    )

Common Parameters
-----------------

All environments accept:

- ``action_mode``: ActionMode - How to control the robot
- ``robot_cls``: Type[Robot] - Robot configuration
- ``render_mode``: str - Rendering mode ("human", "rgb_array", None)
- ``control_frequency``: int - Control loop frequency (Hz)
- ``observation_config``: ObservationConfig - Observation configuration
- ``start_seed``: int - Initial random seed

See Also
--------

- :doc:`../tasks/index` - Task documentation
- :doc:`core` - Base environment class
