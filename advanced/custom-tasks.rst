Creating Custom Tasks
=====================

Learn how to create your own manipulation tasks in RoboEval.

Basic Task Structure
--------------------

1. Create a new file in ``roboeval/envs/``
2. Import required modules
3. Define your environment class
4. Implement required methods

Minimal Example
---------------

.. code-block:: python

    from abc import ABC
    import numpy as np
    from roboeval.roboeval_env import RoboEvalEnv
    from roboeval.const import PRESETS_PATH
    from roboeval.envs.props.items import Cube
    
    class MyCustomTask(RoboEvalEnv, ABC):
        """My custom manipulation task."""
        
        _PRESET_PATH = PRESETS_PATH / "my_task.yaml"  # Optional
        
        def _initialize_env(self):
            """Set up the environment and spawn props."""
            # Create and spawn props
            self.cube = Cube(self._mojo)
            
            # Position the prop
            self.cube.set_pose(position=np.array([0.5, 0.0, 1.0]))
        
        def _on_reset(self):
            """Called on each reset."""
            # Randomize object positions if desired
            x = np.random.uniform(0.3, 0.7)
            y = np.random.uniform(-0.2, 0.2)
            self.cube.set_pose(position=np.array([x, y, 1.0]))
        
        def _success(self):
            """Define success criteria."""
            # Example: cube lifted above table
            cube_pos = self.cube.body.get_position()
            return cube_pos[2] > 1.15
        
        def _fail(self):
            """Define failure criteria."""
            if super()._fail():
                return True
            # Example: cube fell off table
            cube_pos = self.cube.body.get_position()
            if self.cube.is_colliding(self.floor):
                return True
            return False

Required Methods
----------------

``_initialize_env(self)``
~~~~~~~~~~~~~~~~~~~~~~~~~

Set up environment, spawn props, configure scene.

.. code-block:: python

    def _initialize_env(self):
        # Import prop classes
        from roboeval.envs.props.items import Cube
        from roboeval.envs.props.tables import Table
        
        # Create props
        self.table = Table(self._mojo)
        self.cube = Cube(self._mojo)
        
        # Set initial positions using set_pose
        self.cube.set_pose(position=np.array([0.5, 0.0, 1.0]))

``_on_reset(self)``
~~~~~~~~~~~~~~~~~~~

Called each time environment resets.

.. code-block:: python

    def _on_reset(self):
        # Randomize object positions
        if self.randomize_position:
            x = np.random.uniform(0.4, 0.6)
            y = np.random.uniform(-0.1, 0.1)
            self.cube.set_pose(position=np.array([x, y, 1.0]))

``_success(self)``
~~~~~~~~~~~~~~~~~~

Return True if task is successfully completed.

.. code-block:: python

    def _success(self):
        # Check if cube is in goal region
        cube_pos = self.cube.body.get_position()
        goal_pos = np.array([0.5, 0.5, 1.0])
        distance = np.linalg.norm(cube_pos - goal_pos)
        return distance < 0.05

``_fail(self)``
~~~~~~~~~~~~~~~

Return True if task has failed.

.. code-block:: python

    def _fail(self):
        # Call parent's fail check first
        if super()._fail():
            return True
        
        # Check if cube fell off table
        if self.cube.is_colliding(self.floor):
            return True
        
        cube_pos = self.cube.body.get_position()
        return cube_pos[2] < 0.5 or abs(cube_pos[0]) > 1.0

Optional Methods
----------------

``_reward(self)``
~~~~~~~~~~~~~~~~~

Define custom reward function (default is sparse: 1.0 for success, 0.0 otherwise).

.. code-block:: python

    def _reward(self):
        if self.success:
            return 1.0
        
        # Distance-based reward
        cube_pos = self.cube.body.get_position()
        goal_pos = np.array([0.5, 0.5, 1.0])
        distance = np.linalg.norm(cube_pos - goal_pos)
        return -distance

``_on_step(self)``
~~~~~~~~~~~~~~~~~~

Called every step to update metrics (when using MetricRolloutEval).

.. code-block:: python

    def _on_step(self):
        """Update metrics every step."""
        self._metric_step()

Using Presets
-------------

Create a YAML preset file in ``roboeval/envs/presets/``:

.. code-block:: yaml

    # my_task.yaml
    props:
      - type: Table
        position: [0.5, 0.0, 0.0]
        euler: [0, 0, 0]
      - type: Cube
        position: [0.5, 0.0, 1.0]
    
    spawns:
      - name: workspace
        size: [0.4, 0.4, 0.01]
        position: [0.5, 0.0, 1.0]
        euler: [0, 0, 0]

Load preset in your task:

.. code-block:: python

    from roboeval.const import PRESETS_PATH
    
    class MyCustomTask(RoboEvalEnv, ABC):
        _PRESET_PATH = PRESETS_PATH / "my_task.yaml"
        
        def _initialize_env(self):
            # Props from preset are automatically created
            # Access them by type using get_props
            from roboeval.envs.props.tables import Table
            from roboeval.envs.props.items import Cube
            
            # Get props from preset
            tables = self._preset.get_props(Table)
            cubes = self._preset.get_props(Cube)
            
            if tables:
                self.table = tables[0]
            if cubes:
                self.cube = cubes[0]

Creating Variations
-------------------

Create task variations by subclassing:

.. code-block:: python

    class MyCustomTask(RoboEvalEnv, ABC):
        """Base task - static configuration."""
        randomize_position = False
        randomize_orientation = False
        
        def _on_reset(self):
            base_pos = np.array([0.5, 0.0, 0.8])
            
            if self.randomize_position:
                base_pos[0] += np.random.uniform(-0.1, 0.1)
                base_pos[1] += np.random.uniform(-0.1, 0.1)
            
            self.cube.set_pose(position=base_pos)
            
            if self.randomize_orientation:
                angle = np.random.uniform(-np.pi/6, np.pi/6)  # radians
                euler = np.array([0, 0, angle])
                self.cube.set_pose(position=base_pos, euler=euler)
    
    class MyCustomTaskPosition(MyCustomTask):
        """Position randomization."""
        randomize_position = True
    
    class MyCustomTaskOrientation(MyCustomTask):
        """Orientation randomization."""
        randomize_orientation = True
    
    class MyCustomTaskPositionAndOrientation(MyCustomTask):
        """Full randomization."""
        randomize_position = True
        randomize_orientation = True

Tracking Task Progress with MetricRolloutEval
----------------------------------------------

Inherit from ``MetricRolloutEval`` to enable comprehensive metric tracking for your task:

**Basic Setup:**

.. code-block:: python

    from roboeval.roboeval_env import RoboEvalEnv
    from roboeval.utils.metric_rollout import MetricRolloutEval
    from abc import ABC
    
    class MyTask(RoboEvalEnv, ABC, MetricRolloutEval):
        """Task with comprehensive metrics tracking."""
        
        def _initialize_env(self):
            # Create props
            self.cube = Cube(self._mojo)
            
            # Initialize metric tracking
            self._metric_init(
                track_vel_sync=True,              # Track gripper velocity sync
                track_vertical_sync=True,         # Track gripper height alignment
                track_slippage=True,              # Track object slipping
                slip_objects=[self.cube],         # Objects to monitor for slip
                slip_sample_window=20,            # Frames to check for slip
                track_collisions=True,            # Track collisions
                track_cartesian_jerk=True,        # Track end-effector jerk
                track_joint_jerk=True,            # Track joint jerk
                track_cartesian_path_length=True, # Track end-effector path
                track_joint_path_length=True,     # Track joint path
                track_orientation_path_length=True, # Track orientation changes
                robot=self.robot                  # Robot instance
            )
        
        def _on_reset(self):
            super()._on_reset()
            
            # Re-initialize metrics for new episode
            self._metric_init(
                track_vel_sync=True,
                track_vertical_sync=True,
                track_slippage=True,
                slip_objects=[self.cube],
                robot=self.robot,
                slip_sample_window=20,
                track_collisions=True
            )
            
            # Initialize stage flags
            for idx in range(1, 4):
                self._metric_stage(idx, False)
        
        def _on_step(self):
            """Called every step - update metrics."""
            self._metric_step()
        
        def _success(self) -> bool:
            # Check success conditions
            cube_pos = self.cube.body.get_position()
            success = cube_pos[2] > 1.2  # Example: lifted high enough
            
            # Update stage tracking as task progresses
            if self._is_cube_grasped():
                self._metric_stage(1)  # Stage 1: grasped
            
            if cube_pos[2] > 1.2:
                self._metric_stage(2)  # Stage 2: lifted
            
            if success:
                self._metric_stage(3)  # Stage 3: completed
            
            # Finalize metrics and return them
            self._final_metrics = self._metric_finalize(
                success_flag=success,
                target_distance={"lift_distance": cube_pos[2] - 1.0},
                pose_error=0.0  # Example: no orientation constraint
            )
            
            return success
        
        def _get_task_info(self):
            """Expose comprehensive metrics in info dict."""
            return getattr(self, "_final_metrics", {})

**Available Tracking Options:**

- ``track_vel_sync``: Bimanual arm velocity synchronization
- ``track_vertical_sync``: Bimanual gripper height alignment
- ``track_slippage``: Object grip loss detection
- ``track_collisions``: Environment and self-collision events
- ``track_cartesian_jerk``: End-effector jerk (smoothness)
- ``track_joint_jerk``: Joint space jerk (smoothness)
- ``track_cartesian_path_length``: Total end-effector path traveled
- ``track_joint_path_length``: Total joint space path traveled
- ``track_orientation_path_length``: Total orientation change

**Metrics Returned by _metric_finalize():**

.. code-block:: python

    metrics = {
        "success": 1.0,  # Success flag
        "completion_time": 15.3,  # Episode duration (seconds)
        
        # Slip tracking
        "slip_count": 2,
        "slip_count_per_object": {"object_1": 2},
        
        # Collision tracking
        "env_collision_count": 1,
        "self_collision_count": 0,
        
        # Stage progression
        "task_stage_reached": {1: True, 2: True, 3: True},
        "subtask_progress": 1.0,  # 3/3 stages completed
        
        # Custom distances and errors
        "target_distance": {"lift_distance": 0.15, ...},
        "object_pose_error": 0.02,
        
        # Bimanual coordination (if multiarm)
        "bimanual_arm_velocity_difference": 0.05,
        "bimanual_gripper_vertical_difference": 0.01,
        
        # Path lengths
        "cartesian_path_length": {"left": 1.5, "right": 1.6},
        "total_cartesian_path_length": 3.1,
        "joint_path_length": {"left": 8.2, "right": 8.5},
        
        # Smoothness (jerk)
        "avg_cartesian_jerk": {"left": 0.3, "right": 0.4},
        "rms_cartesian_jerk": {"left": 0.5, "right": 0.6},
    }

**Stage Tracking:**

.. code-block:: python

    def _success(self):
        # Update stages as task progresses
        if self._is_object_grasped():
            self._metric_stage(1)  # Mark stage 1 complete
        
        if self.object.body.get_position()[2] > 1.5:
            self._metric_stage(2)  # Mark stage 2 complete
        
        if self._in_goal_region():
            self._metric_stage(3)  # Mark stage 3 complete
        
        # Finalize returns subtask_progress = completed_stages / max_stage
        metrics = self._metric_finalize(success_flag=self._in_goal_region())
        return self._in_goal_region()

Complete Example
----------------

.. code-block:: python

    from abc import ABC
    import numpy as np
    from roboeval.roboeval_env import RoboEvalEnv
    from roboeval.utils.metric_rollout import MetricRolloutEval
    from roboeval.envs.props.items import Cube
    from roboeval.envs.props.tables import Table
    
    class PickAndPlace(RoboEvalEnv, ABC, MetricRolloutEval):
        """Pick a cube and place it in goal region with comprehensive metrics."""
        
        randomize_position = False
        
        def _initialize_env(self):
            self.table = Table(self._mojo)
            self.cube = Cube(self._mojo)
            
            self.table.set_pose(position=np.array([0.5, 0.0, 0.0]))
            self.goal_pos = np.array([0.5, 0.5, 0.8])
            
            # Initialize metrics tracking
            self._metric_init(
                track_slippage=True,
                slip_objects=[self.cube],
                track_collisions=True,
                track_cartesian_path_length=True,
                track_cartesian_jerk=True,
                robot=self.robot,
                slip_sample_window=20
            )
        
        def _on_reset(self):
            if self.randomize_position:
                x = np.random.uniform(0.3, 0.7)
                y = np.random.uniform(-0.2, 0.2)
                self.cube.set_pose(position=np.array([x, y, 0.8]))
            else:
                self.cube.set_pose(position=np.array([0.5, 0.0, 0.8]))
            
            # Re-initialize metrics for new episode
            self._metric_init(
                track_slippage=True,
                slip_objects=[self.cube],
                track_collisions=True,
                track_cartesian_path_length=True,
                track_cartesian_jerk=True,
                robot=self.robot,
                slip_sample_window=20
            )
            
            # Initialize stages
            for idx in range(1, 3):
                self._metric_stage(idx, False)
        
        def _on_step(self):
            """Update metrics every step."""
            self._metric_step()
        
        def _success(self):
            cube_pos = self.cube.body.get_position()
            distance = np.linalg.norm(cube_pos - self.goal_pos)
            success = distance < 0.05
            
            # Track stages
            if self._is_cube_grasped():
                self._metric_stage(1)  # Grasped
            
            if success:
                self._metric_stage(2)  # Placed in goal
            
            # Finalize metrics
            self._final_metrics = self._metric_finalize(
                success_flag=success,
                target_distance={"distance_to_goal": distance},
                pose_error=0.0
            )
            
            return success
        
        def _fail(self):
            cube_pos = self.cube.body.get_position()
            if cube_pos[2] < 0.0:
                super()._fail()
                return True
            return False
        
        def _get_task_info(self):
            """Return comprehensive metrics from MetricRolloutEval."""
            return getattr(self, "_final_metrics", {})
        
        def _reward(self):
            """Calculate reward based on cube-goal distance."""
            if self.success:
                return 1.0
            cube_pos = self.cube.body.get_position()
            distance = np.linalg.norm(cube_pos - self.goal_pos)
            return -distance
    
    class PickAndPlacePosition(PickAndPlace):
        randomize_position = True

Testing Your Task
-----------------

.. code-block:: python

    from roboeval.action_modes import JointPositionActionMode
    from roboeval.robots.configs.panda import BimanualPanda
    
    env = PickAndPlace(
        action_mode=JointPositionActionMode(),
        render_mode="human",
        robot_cls=BimanualPanda
    )
    
    obs, info = env.reset()
    
    for step in range(1000):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        
        if terminated or truncated:
            # Access comprehensive metrics at episode end
            print(f"Success: {info['success']}")
            print(f"Completion time: {info['completion_time']:.2f}s")
            print(f"Stages completed: {info.get('subtask_progress', 0):.1%}")
            break

Analyzing Task Performance
--------------------------

**Accessing metrics during execution:**

.. code-block:: python

    obs, reward, terminated, truncated, info = env.step(action)
    
    if terminated or truncated:
        # Comprehensive metrics available at episode end
        print(f"Success: {info['success']}")
        print(f"Completion time: {info['completion_time']:.2f}s")
        print(f"Slips: {info['slip_count']}")
        print(f"Env collisions: {info.get('env_collision_count', 0)}")
        print(f"Subtask progress: {info['subtask_progress']:.1%}")
        
        if "cartesian_path_length" in info:
            print(f"Path lengths: {info['cartesian_path_length']}")
        
        if "avg_cartesian_jerk" in info:
            print(f"Jerk (smoothness): {info['avg_cartesian_jerk']}")

**Collecting metrics over episodes:**

.. code-block:: python

    from collections import defaultdict
    import numpy as np
    
    metrics = defaultdict(list)
    
    for episode in range(100):
        obs, info = env.reset()
        
        for step in range(1000):
            action = policy.predict(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            
            if terminated or truncated:
                # Collect episode metrics
                metrics["success"].append(info["success"])
                metrics["completion_time"].append(info["completion_time"])
                metrics["slip_count"].append(info["slip_count"])
                metrics["subtask_progress"].append(info["subtask_progress"])
                
                if "total_cartesian_path_length" in info:
                    metrics["path_length"].append(info["total_cartesian_path_length"])
                
                if "env_collision_count" in info:
                    metrics["collisions"].append(info["env_collision_count"])
                
                break
    
    # Analyze results
    print(f"Success rate: {np.mean(metrics['success']):.2%}")
    print(f"Avg completion time: {np.mean(metrics['completion_time']):.2f}s")
    print(f"Avg slip events: {np.mean(metrics['slip_count']):.2f}")
    print(f"Avg subtask progress: {np.mean(metrics['subtask_progress']):.1%}")
    print(f"Avg path length: {np.mean(metrics['path_length']):.3f}")
    print(f"Avg collisions: {np.mean(metrics['collisions']):.2f}")

Best Practices
--------------

1. **Start simple** - Test with static configuration first
2. **Inherit from MetricRolloutEval** - Enables comprehensive metric tracking (collisions, jerk, path length, slippage, etc.)
3. **Define clear stages** - Break tasks into measurable progression steps using ``_metric_stage()``
4. **Track what matters**:
   
   - Distance to goal for pick-and-place tasks (via ``target_distance`` in ``_metric_finalize()``)
   - Orientation error for alignment tasks (via ``pose_error`` in ``_metric_finalize()``)
   - Bimanual coordination for two-arm tasks (``track_vel_sync``, ``track_vertical_sync``)
   - Smoothness for trajectory quality (``track_cartesian_jerk``, ``track_joint_jerk``)
   - Slippage for grasping tasks (``track_slippage`` with ``slip_objects``)
   - Collisions for safety (``track_collisions``)

5. **Initialize metrics properly**:
   
   - Call ``_metric_init()`` in both ``_initialize_env()`` and ``_on_reset()``
   - Call ``_metric_step()`` in ``_on_step()``
   - Call ``_metric_finalize()`` in ``_success()`` before returning
   - Store result in ``self._final_metrics`` and return via ``_get_task_info()``

6. **Test thoroughly** - Verify success/fail conditions with edge cases
7. **Add variations gradually** - Start static, then add randomization
8. **Document metrics** - Explain what each tracked metric represents in your task docstring

See Also
--------

- :doc:`custom-props` - Create custom objects
- :doc:`custom-robots` - Configure robots
- :doc:`metrics` - Metrics and evaluation details
- ``roboeval/utils/metric_rollout.py`` - Full MetricRolloutEval API reference
