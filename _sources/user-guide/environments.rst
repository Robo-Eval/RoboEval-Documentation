Environments
============

RoboEval provides a variety of bimanual manipulation environments built on the Gymnasium API. Each environment represents a real-world manipulation task with varying levels of difficulty.

Environment Basics
------------------

All RoboEval environments inherit from ``RoboEvalEnv`` and follow the standard Gymnasium interface:

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPot
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.robots.configs.panda import BimanualPanda
    
    env = LiftPot(
        action_mode=JointPositionActionMode(),
        render_mode="human",
        robot_cls=BimanualPanda,
        control_frequency=20
    )
    
    obs, info = env.reset()
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

Environment Parameters
----------------------

**Required Parameters:**

``action_mode`` : ActionMode
    Defines how the robot is controlled (joint positions, end-effector poses, etc.)

**Optional Parameters:**

``render_mode`` : str, optional
    Rendering mode: ``"human"`` (window), ``"rgb_array"`` (images), or ``None``

``robot_cls`` : Type[Robot], default=BimanualPanda
    Robot configuration to use

``control_frequency`` : int, default=500
    Control loop frequency in Hz (typically set to 20 for data collection)

``observation_config`` : ObservationConfig
    Configuration for observations including cameras

``start_seed`` : int, optional
    Initial random seed for reproducibility

Task Families
-------------

LiftPot
~~~~~~~

Grasp a kitchen pot by both handles and lift it above the table without tilting or colliding with cabinets.

**Success Criteria:**
- Pot lifted at least 10cm above initial height
- Pot orientation maintained (no excessive tilting)
- No collision with cabinets or floor

**Variations:**

- ``LiftPot`` - Static position
- ``LiftPotPosition`` - Random position on table
- ``LiftPotOrientation`` - Random orientation (±30°)
- ``LiftPotPositionAndOrientation`` - Both randomized

.. code-block:: python

    from roboeval.envs.lift_pot import (
        LiftPot, LiftPotPosition, 
        LiftPotOrientation, LiftPotPositionAndOrientation
    )

Stack Books
~~~~~~~~~~~

Two related tasks involving book manipulation:

**StackSingleBookShelf:**

Pick up a book from a counter and place it on a bookshelf (upper or lower shelf).

**Success Criteria:**
- Book must be in contact with either upper or lower shelf
- Gripper must release the book

- ``StackSingleBookShelf``
- ``StackSingleBookShelfPosition``
- ``StackSingleBookShelfPositionAndOrientation``

**PickSingleBookFromTable:**

Pick up a book from a counter and hold it lifted.

**Success Criteria:**
- Book lifted off the counter
- At least one gripper holding the book
- Book not colliding with counter or floor

- ``PickSingleBookFromTable``
- ``PickSingleBookFromTablePosition``
- ``PickSingleBookFromTableOrientation``
- ``PickSingleBookFromTablePositionAndOrientation``

.. code-block:: python

    from roboeval.envs.stack_books import (
        StackSingleBookShelf,
        PickSingleBookFromTable
    )

Manipulation Tasks
~~~~~~~~~~~~~~~~~~

Basic manipulation primitives:

**StackTwoBlocks:**

Stack one cube on top of another cube.

**Success Criteria:**
- One cube positioned on top of the other
- Cubes not colliding with floor

- ``StackTwoBlocks``
- ``StackTwoBlocksPosition``
- ``StackTwoBlocksOrientation``
- ``StackTwoBlocksPositionAndOrientation``

**CubeHandover:**

Transfer a rod/cube from one gripper to the other gripper.

**Success Criteria:**
- Object must transfer from initial gripper to opposite gripper
- Initial gripper must release, opposite gripper must grasp
- Object not dropped to floor

- ``CubeHandover``
- ``CubeHandoverPosition``
- ``CubeHandoverOrientation``
- ``CubeHandoverPositionAndOrientation``

**VerticalCubeHandover:**

Handover a rod while maintaining vertical alignment (similar to CubeHandover).

.. code-block:: python

    from roboeval.envs.manipulation import (
        StackTwoBlocks, CubeHandover, VerticalCubeHandover
    )

RotateValve
~~~~~~~~~~~

Rotate valve wheels using bimanual coordination.

**Success Criteria:**
- Both valve wheels rotated to target positions
- Coordinated bimanual manipulation

**Variations:**

- ``RotateValve``
- ``RotateValvePosition``
- ``RotateValvePositionAndOrientation``

.. code-block:: python

    from roboeval.envs.rotate_utility_objects import (
        RotateValve, RotateValvePosition
    )

PackBox
~~~~~~~

Close the lid flaps of a packaging box using both arms.

**Success Criteria:**
- Both left and right flaps closed (joint states near 0)
- Bimanual coordination required to close both flaps

**Variations:**

- ``PackBox``
- ``PackBoxPosition``
- ``PackBoxOrientation``
- ``PackBoxPositionAndOrientation``

.. code-block:: python

    from roboeval.envs.pack_objects import (
        PackBox, PackBoxPosition
    )

LiftTray
~~~~~~~~

Grasp and lift a breakfast tray using both grippers simultaneously.

**Success Criteria:**
- Both grippers holding the tray
- Tray lifted off the table (no collision)
- Coordinated bimanual lifting

**Variations:**

- ``LiftTray``
- ``LiftTrayPosition``
- ``LiftTrayOrientation``
- ``LiftTrayPositionAndOrientation``
- ``DragOverAndLiftTray`` - Drag tray over an obstacle first

.. code-block:: python

    from roboeval.envs.lift_tray import (
        LiftTray, DragOverAndLiftTray
    )

Understanding Variations
------------------------

Most tasks come in 4 variations:

1. **Base Task** - Objects in fixed positions
2. **Position** - Random position within workspace
3. **Orientation** - Random orientation (typically ±30° around Z-axis)
4. **Position and Orientation** - Both randomized

This allows you to progressively increase difficulty and test generalization.

Observation Space
-----------------

The default observation space includes:

.. code-block:: python

    {
        'proprioception': Box(shape=(n_qpos + n_qvel,)),  # Joint positions + velocities
        'proprioception_grippers': Box(shape=(n_grippers,)),  # Gripper positions
    }

For robots with floating bases, additional observations are included:

.. code-block:: python

    {
        'proprioception_floating_base': Box(shape=(floating_base_dof,)),
        'proprioception_floating_base_actions': Box(shape=(floating_base_dof,)),
    }

With cameras enabled:

.. code-block:: python

    from roboeval.utils.observation_config import ObservationConfig, CameraConfig
    
    obs_config = ObservationConfig(
        cameras=[
            CameraConfig(
                name="external",
                rgb=True,
                depth=True,
                resolution=(256, 256)
            )
        ]
    )

The observation will additionally include:

.. code-block:: python

    {
        'external_rgb': Box(shape=(256, 256, 3)),
        'external_depth': Box(shape=(256, 256, 1)),
    }

Action Space
------------

Action space depends on the chosen ``action_mode``:

**JointPositionActionMode:**

.. code-block:: python

    # Absolute joint positions
    action_space = Box(low=-3.14, high=3.14, shape=(n_joints,))
    
    # Delta (incremental) positions
    action_space = Box(low=-0.1, high=0.1, shape=(n_joints,))
    
    # End-effector mode (absolute)
    action_space = Box(low=-np.inf, high=np.inf, shape=(n_ee_dims,))
    
    # End-effector mode (delta)
    action_space = Box(low=-0.1, high=0.1, shape=(n_ee_dims,))

Reward Structure
----------------

RoboEval uses sparse rewards by default:

- ``1.0`` for task success
- ``0.0`` otherwise

Access task-specific metrics via the ``info`` dictionary:

.. code-block:: python

    obs, reward, terminated, truncated, info = env.step(action)
    
    # Always available
    print(f"Task success: {info['task_success']}")
    
    # Task-specific metrics (varies by environment)
    # Most environments expose these at episode end via _final_metrics
    if info:
        for key, value in info.items():
            print(f"{key}: {value}")

Episode Termination
-------------------

Episodes terminate when:

1. **Success** - Task successfully completed (``terminated=True``)
2. **Failure** - Task failed (object dropped, collision, etc.) (``terminated=True``)
3. **Instability** - Physics simulation becomes unstable (``truncated=True``)

Check termination reason:

.. code-block:: python

    if terminated:
        if info.get('task_success'):
            print("Task completed successfully!")
        else:
            print("Task failed")
    elif truncated:
        print("Episode truncated (physics instability)")

Environment Configuration
-------------------------

**Render Modes:**

.. code-block:: python

    # Interactive viewer (for debugging)
    env = LiftPot(render_mode="human")
    
    # RGB array (for video recording)
    env = LiftPot(render_mode="rgb_array")
    
    # No rendering (fastest)
    env = LiftPot(render_mode=None)

**Control Frequency:**

.. code-block:: python

    # High frequency (default, for simulation)
    env = LiftPot(control_frequency=500)
    
    # Low frequency (for data collection, matching demos)
    env = LiftPot(control_frequency=20)

**Random Seeds:**

.. code-block:: python

    # Reproducible episodes
    env = LiftPot(start_seed=42)
    obs, info = env.reset(seed=42)

Best Practices
--------------

1. **Match control frequency** to your demonstrations (typically 20 Hz)
2. **Use render_mode="human"** for debugging, None for training
3. **Check info dict** for detailed metrics and debugging information
4. **Start with base tasks** before trying randomized variations
5. **Set random seeds** for reproducible experiments

Next Steps
----------

- Learn about :doc:`action-modes` in detail
- Configure :doc:`observations` for your needs
- Explore :doc:`data-collection` tools
- See :doc:`../tasks/index` for complete task documentation
