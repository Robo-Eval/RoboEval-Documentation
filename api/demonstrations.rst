Demonstrations API
==================

Classes and utilities for working with demonstration data in RoboEval.

Demo
----

.. autoclass:: roboeval.demonstrations.Demo
   :members:
   :undoc-members:
   :show-inheritance:

   The ``Demo`` class stores demonstration data with the following structure:

   **Attributes:**

   - ``metadata`` (``Metadata``): Contains environment configuration, task information, and robot configuration
   - ``timesteps`` (``list[DemoStep]``): List of demonstration timesteps
   
   **Key Methods:**

   - ``from_safetensors(demo_path, override_metadata=None)``: Load demonstration from a safetensors file
   - ``from_env(env)``: Create demonstration by recording from an environment
   - ``save(path, debug=False)``: Save demonstration to disk in safetensors format

DemoStep
--------

.. autoclass:: roboeval.demonstrations.DemoStep
   :members:
   :undoc-members:
   :show-inheritance:

   The ``DemoStep`` class represents a single timestep in a demonstration.

   **Attributes:**

   - ``observation`` (``dict[str, Any]``): Dictionary containing observations at this timestep
   - ``reward`` (``float``): Reward received at this timestep
   - ``termination`` (``bool``): Whether the episode terminated
   - ``truncation`` (``bool``): Whether the episode was truncated
   - ``info`` (``dict[str, Any]``): Additional information (includes executed action under ``"action"`` key)

   **Key Properties:**

   - ``executed_action``: The action that was executed to reach this timestep (accessed from ``info`` dict)
   - ``has_visual_observations``: Check if this timestep contains visual observations
   - ``visual_observations``: Get all visual observations from this timestep

DemoConverter
-------------

.. autoclass:: roboeval.demonstrations.DemoConverter
   :members:
   :undoc-members:
   :show-inheritance:

   The ``DemoConverter`` class provides static methods for converting demonstrations between different action representations.

   **Available Conversion Methods:**

   - ``absolute_to_delta(demo)``: Convert absolute joint position actions to delta actions
   - ``joint_to_ee(demo)``: Convert joint position actions to end-effector position actions
   - ``joint_absolute_to_ee_delta(demo)``: Convert absolute joint positions to delta end-effector positions
   - ``clip_actions(demo, action_scale=1)``: Clip demonstration actions to action space limits
   - ``decimate(demo, target_freq, original_freq=20, robot=None)``: Decimate demonstration to lower control frequency
   - ``create_demo_in_new_env(demo, env, demo_frequency=20)``: Replay demonstration in a new environment configuration

DemoStore
---------

.. autoclass:: roboeval.demonstrations.DemoStore
   :members:
   :undoc-members:
   :show-inheritance:

   The ``DemoStore`` class provides methods for loading demonstrations from disk or cache.

   **Key Methods:**

   - ``get_demos(metadata, amount=None, frequency=20)``: Load demonstrations matching metadata
   - ``get_demos_from_folder(demos_dir, metadata, amount=None, frequency=20)``: Load demonstrations from a specific folder
   - ``load_demo_from_path(demo_path, metadata, frequency=20)``: Load a single demonstration from path
   - ``cache_demo(demo, frequency=None)``: Cache a demonstration for faster loading
   - ``list_demo_paths(metadata)``: List paths of all demonstrations matching metadata
   - ``demo_exists(metadata, frequency=None)``: Check if demonstration exists
   - ``pull_demos()``: Download demonstrations from remote storage

DemoPlayer
----------

.. autoclass:: roboeval.demonstrations.DemoPlayer
   :members:
   :undoc-members:
   :show-inheritance:

   The ``DemoPlayer`` class provides methods for replaying and validating demonstrations in environments.

   **Key Methods:**

   - ``replay(demo, demo_frequency=20)``: Replay a demonstration and create a new environment
   - ``replay_in_env(demo, env, demo_frequency=20)``: Replay a demonstration in an existing environment
   - ``replay_in_env_save_position_orientation(demo, env, demo_frequency=20)``: Replay and save position/orientation data
   - ``validate(demo, demo_frequency=20)``: Validate demonstration by replaying it
   - ``validate_in_env(demo, env, demo_frequency=20)``: Validate demonstration in an existing environment

Metadata
--------

.. autoclass:: roboeval.demonstrations.utils.Metadata
   :members:
   :undoc-members:
   :show-inheritance:

   The ``Metadata`` class stores task and environment configuration information for demonstrations.

   **Attributes:**

   - ``observation_mode`` (``ObservationMode``): Type of observations (State, Pixel, or Lightweight)
   - ``environment_data`` (``EnvData``): Environment configuration data
   - ``seed`` (``int``): Random seed used
   - ``package_versions`` (``dict[str, str]``): Versions of tracked packages
   - ``date`` (``str``): Timestamp of creation
   - ``uuid`` (``str``): Unique identifier

   **Key Methods:**

   - ``from_env(env, is_lightweight=False)``: Create metadata from an environment
   - ``from_env_cls(env_cls, action_mode, ...)``: Create metadata from environment class
   - ``from_safetensors(path)``: Load metadata from a safetensors file
   - ``ready_for_safetensors()``: Prepare metadata for safetensors serialization
   - ``get_env(control_frequency, render_mode=None)``: Create environment from metadata
   - ``get_action_mode()``: Get action mode from metadata
   - ``get_robot()``: Get robot instance from metadata
   - ``get_action_space(action_scale)``: Get action space from metadata

   **Key Properties:**

   - ``env_name``: Environment name
   - ``env_cls``: Environment class
   - ``robot_cls``: Robot class
   - ``action_mode_cls``: Action mode class
   - ``filename``: Generated filename for saving
   - ``floating_dof_count``: Count of floating degrees of freedom

See Also
--------

- :doc:`../user-guide/demonstrations` - Demonstrations user guide
- :doc:`../getting-started/examples` - Example scripts showing demo usage

