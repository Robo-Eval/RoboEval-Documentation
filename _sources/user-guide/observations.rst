Observations
============

Configure what information the environment returns at each step.

Observation Configuration
--------------------------

Create custom observation configurations:

.. code-block:: python

    from roboeval.utils.observation_config import ObservationConfig, CameraConfig
    
    obs_config = ObservationConfig(
        cameras=[
            CameraConfig(
                name="external",
                rgb=True,
                depth=True,
                resolution=(256, 256),
                pos=(0.0, 2.0, 1.5),
                quat=(1, 0, 0, 0)
            ),
            CameraConfig(
                name="wrist_left",
                rgb=True,
                depth=False,
                resolution=(128, 128)
            )
        ],
        proprioception=True,
        privileged_information=False
    )
    
    env = LiftPot(
        action_mode=JointPositionActionMode(),
        observation_config=obs_config,
        robot_cls=BimanualPanda
    )

Default Observations
--------------------

Without custom configuration (default: ``proprioception=True``), observations include:

.. code-block:: python

    obs = {
        'proprioception': array([...]),  # Joint positions + velocities concatenated
        'proprioception_grippers': array([...]),  # Gripper positions
    }

For robots with floating bases, additional observations are included:

.. code-block:: python

    obs = {
        'proprioception': array([...]),
        'proprioception_grippers': array([...]),
        'proprioception_floating_base': array([...]),  # Base position/orientation
        'proprioception_floating_base_actions': array([...]),  # Base action DOFs
    }

ObservationConfig Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``proprioception`` : bool, default=True
    Include robot joint positions and velocities

``privileged_information`` : bool, default=False
    Include task-specific privileged observations (e.g., object poses)

``cameras`` : List[CameraConfig], default=[]
    List of camera configurations for visual observations

Camera Observations
-------------------

Add visual observations with cameras:

.. code-block:: python

    obs_config = ObservationConfig(
        cameras=[
            CameraConfig(
                name="external",
                rgb=True,
                depth=True,
                resolution=(256, 256),
                pos=(0.0, 2.0, 1.5),
                quat=(1, 0, 0, 0)
            )
        ],
        proprioception=True
    )

Observation includes:

.. code-block:: python

    obs = {
        'proprioception': array([...]),
        'proprioception_grippers': array([...]),
        'external_rgb': array([256, 256, 3]),    # RGB image
        'external_depth': array([256, 256, 1]),  # Depth map
    }

CameraConfig Parameters
~~~~~~~~~~~~~~~~~~~~~~~

``name`` : str
    Camera name (must exist in environment). Available cameras: ``"external"``, ``"wrist_left"``, ``"wrist_right"``, ``"head"`` (depending on robot configuration)

``rgb`` : bool, default=True
    Include RGB images

``depth`` : bool, default=False
    Include depth maps

``resolution`` : tuple[int, int], default=(128, 128)
    Image resolution (width, height)

``pos`` : tuple[float, float, float], optional
    Camera position (x, y, z). If not specified, uses default camera position.

``quat`` : tuple[float, float, float, float], optional
    Camera orientation as quaternion (w, x, y, z). If not specified, uses default camera orientation.

Multiple Cameras
----------------

.. code-block:: python

    obs_config = ObservationConfig(
        cameras=[
            CameraConfig(name="external", rgb=True, resolution=(256, 256)),
            CameraConfig(name="wrist_left", rgb=True, resolution=(128, 128)),
            CameraConfig(name="wrist_right", rgb=True, resolution=(128, 128)),
        ],
        proprioception=True
    )

Privileged Information
----------------------

Enable task-specific privileged observations (e.g., ground-truth object poses):

.. code-block:: python

    obs_config = ObservationConfig(
        proprioception=True,
        privileged_information=True
    )

Note: Privileged information varies by task and is defined in each environment's ``_get_task_privileged_obs()`` method.

Best Practices
--------------

1. **Lower resolution** for faster training (64x64 or 128x128)
2. **Higher resolution** for evaluation (256x256)
3. **Depth maps** for 3D reasoning tasks
4. **Multiple viewpoints** for better spatial understanding

Next Steps
----------

- Learn about :doc:`data-collection`
- See :doc:`demonstrations` for replay
