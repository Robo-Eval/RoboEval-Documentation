Core API
========

Core RoboEval environment class.

RoboEvalEnv
-----------

.. autoclass:: roboeval.roboeval_env.RoboEvalEnv
   :members:
   :undoc-members:
   :show-inheritance:

   Base environment class that all RoboEval tasks inherit from. Provides a Gymnasium-compatible interface with integrated robot control, observation collection, and rendering.

   **Initialization Parameters:**

   - ``action_mode`` (``ActionMode``): Defines how the robot is controlled
   - ``robot_cls`` (``Type[Robot]``): Robot configuration class (e.g., ``BimanualPanda``)
   - ``render_mode`` (``str``): Rendering mode - ``"human"``, ``"rgb_array"``, or ``None``
   - ``control_frequency`` (``int``): Control loop frequency in Hz (default: 20)
   - ``observation_config`` (``ObservationConfig``): Configuration for observations
   - ``start_seed`` (``int``): Initial random seed

   **Key Methods:**

   - ``reset(seed=None, options=None)``: Reset environment to initial state, returns ``(observation, info)``
   - ``step(action)``: Execute one environment step, returns ``(observation, reward, terminated, truncated, info)``
   - ``render()``: Render the current environment state
   - ``close()``: Clean up environment resources
   - ``get_spawn_boundary(name)``: Get spawn boundary by name

   **Key Properties:**

   - ``action_space``: Gymnasium action space (``Box``)
   - ``observation_space``: Gymnasium observation space (``Dict``)
   - ``robot``: Robot instance
   - ``mojo``: Mojo physics instance
   - ``task_name``: Environment class name
   - ``success``: Whether current step is successful
   - ``fail``: Whether current step has failed
   - ``reward``: Current step reward
   - ``terminate``: Termination condition
   - ``truncate``: Truncation condition
   - ``is_healthy``: Whether simulation is healthy
   - ``observation_config``: Observation configuration
   - ``control_frequency``: Control frequency in Hz
   - ``floor``: Floor geometry element
   - ``action``: Last executed action
   - ``seed``: Current seed

Example Usage
-------------

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPot
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.robots.configs.panda import BimanualPanda
    
    env = LiftPot(
        action_mode=JointPositionActionMode(),
        robot_cls=BimanualPanda,
        render_mode="human"
    )
    
    obs, info = env.reset()
    for _ in range(100):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            break
    env.close()

See Also
--------

- :doc:`environments` - Task-specific environment classes
- :doc:`../user-guide/environments` - Environment usage guide
- :doc:`../getting-started/quickstart` - Quick start tutorial

