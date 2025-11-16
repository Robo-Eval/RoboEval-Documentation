Utils API
=========

Utility classes and functions for RoboEval.

ObservationConfig
-----------------

.. autoclass:: roboeval.utils.observation_config.ObservationConfig
   :members:
   :undoc-members:
   :show-inheritance:

   Configuration for environment observations.

   **Attributes:**

   - ``cameras`` (``list[CameraConfig]``): List of camera configurations
   - ``proprioception`` (``bool``): Whether to include proprioceptive observations (default: True)
   - ``privileged_information`` (``bool``): Whether to include privileged information (default: False)

   **Example:**

   .. code-block:: python

       from roboeval.utils.observation_config import ObservationConfig, CameraConfig
       
       obs_config = ObservationConfig(
           cameras=[
               CameraConfig(
                   name="external",
                   rgb=True,
                   depth=True,
                   resolution=(256, 256),
                   pos=(0.0, 2.0, 1.5)
               )
           ],
           proprioception=True
       )

CameraConfig
------------

.. autoclass:: roboeval.utils.observation_config.CameraConfig
   :members:
   :undoc-members:
   :show-inheritance:

   Configuration for individual camera observations.

   **Attributes:**

   - ``name`` (``str``): Camera identifier
   - ``rgb`` (``bool``): Enable RGB images (default: True)
   - ``depth`` (``bool``): Enable depth maps (default: False)
   - ``resolution`` (``tuple[int, int]``): Image resolution as (width, height) (default: (128, 128))
   - ``pos`` (``Optional[tuple[float, float, float]]``): Camera position as (x, y, z)
   - ``quat`` (``Optional[tuple[float, float, float, float]]``): Camera orientation quaternion

MetricRolloutEval
-----------------

.. autoclass:: roboeval.utils.metric_rollout.MetricRolloutEval
   :members:
   :undoc-members:
   :show-inheritance:

   Base class for tasks with comprehensive metric tracking capabilities.

   Tasks should inherit from this class and call metric tracking methods to collect detailed performance metrics beyond task success.

   **Key Methods:**

   - ``_metric_init(...)``: Initialize metric tracking (called once at environment initialization)
   - ``_metric_step()``: Update metrics at each step (called every environment step)
   - ``_metric_stage()``: Record metrics at stage transitions (optional)
   - ``_metric_finalize()``: Compute final metrics (called at episode end, returns dict)

   **Tracking Options:**

   The ``_metric_init()`` method accepts the following tracking options:

   - ``track_vel_sync`` (``bool``): Track gripper actuator speed synchronization
   - ``track_vertical_sync`` (``bool``): Track gripper wrist height alignment
   - ``track_slippage`` (``bool``): Track object slippage from grippers
   - ``slip_objects`` (``Optional[list]``): List of props to monitor for grip loss
   - ``slip_sample_window`` (``int``): Number of frames for slip detection (default: 20)
   - ``track_collisions`` (``bool``): Track environment and self-collisions
   - ``track_cartesian_jerk`` (``bool``): Track end-effector jerk (default: True)
   - ``track_joint_jerk`` (``bool``): Track joint jerk (default: True)
   - ``track_cartesian_path_length`` (``bool``): Track total end-effector path length (default: True)
   - ``track_joint_path_length`` (``bool``): Track total joint space path length (default: True)
   - ``track_orientation_path_length`` (``bool``): Track total orientation change (default: True)
   - ``robot`` (``Robot``): Robot instance for accessing kinematics

   See :doc:`../advanced/metrics` for detailed usage and interpretation.

EnvHealth
---------

.. autoclass:: roboeval.utils.env_health.EnvHealth
   :members:
   :undoc-members:
   :show-inheritance:

   Monitor physics simulation stability and detect unstable simulations.

   **Exception Classes:**

   - ``UnstableSimulationWarning``: Warning for minor simulation instabilities
   - ``UnstableSimulationError``: Error for critical simulation failures

Geometry Utilities
------------------

.. automodule:: roboeval.utils.geometry
   :members:
   :undoc-members:

   Geometry and collision detection utilities.

   **Key Functions:**

   - ``check_obb_intersection(pos1, rot1, size1, pos2, rot2, size2)``: Check oriented bounding box intersection
   - ``check_sites_intersection(...)``: Check intersection between sites
   - ``check_sites_intersection_mojo(...)``: Check intersection using Mojo physics

See Also
--------

- :doc:`core` - Core RoboEval API
- :doc:`../user-guide/observations` - Observation configuration guide
- :doc:`../advanced/metrics` - Metrics tracking guide

