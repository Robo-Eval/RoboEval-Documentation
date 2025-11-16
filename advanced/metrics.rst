Metrics
=======

RoboEval provides comprehensive metrics tracking through the ``MetricRolloutEval`` class, enabling detailed analysis of robot performance beyond binary success.

Overview
--------

The metrics system tracks:

- **Task success and progression** (stages, subtask completion)
- **Bimanual coordination** (velocity sync, vertical alignment)
- **Object manipulation quality** (slippage detection)
- **Safety** (collision detection)
- **Trajectory quality** (smoothness via jerk metrics)
- **Efficiency** (path length in cartesian and joint space)
- **Custom task metrics** (distances, pose errors)

MetricRolloutEval Integration
------------------------------

To enable comprehensive metrics, inherit from ``MetricRolloutEval`` in your task:

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
                track_vel_sync=True,
                track_vertical_sync=True,
                track_slippage=True,
                slip_objects=[self.cube],
                slip_sample_window=20,
                track_collisions=True,
                track_cartesian_jerk=True,
                track_joint_jerk=True,
                track_cartesian_path_length=True,
                track_joint_path_length=True,
                track_orientation_path_length=True,
                robot=self.robot
            )
        
        def _on_reset(self):
            super()._on_reset()
            # Re-initialize metrics for each episode
            self._metric_init(...)
            
            # Initialize stage flags
            for idx in range(1, 4):
                self._metric_stage(idx, False)
        
        def _on_step(self):
            # Update metrics every step
            self._metric_step()
        
        def _success(self):
            success = self._check_success_conditions()
            
            # Track stage progression
            if self._is_grasped():
                self._metric_stage(1)
            if self._is_lifted():
                self._metric_stage(2)
            if success:
                self._metric_stage(3)
            
            # Finalize and store metrics
            self._final_metrics = self._metric_finalize(
                success_flag=success,
                target_distance={"distance": 0.1},
                pose_error=0.02
            )
            
            return success
        
        def _get_task_info(self):
            # Expose metrics via info dict
            return getattr(self, "_final_metrics", {})

        def _get_task_info(self):
            # Expose metrics via info dict
            return getattr(self, "_final_metrics", {})

Available Tracking Options
---------------------------

``_metric_init()`` Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Bimanual Coordination:**

- ``track_vel_sync`` (bool): Track arm velocity synchronization
  
  - Measures difference in joint velocities between left and right arms
  - Returns ``bimanual_arm_velocity_difference`` (lower is better)

- ``track_vertical_sync`` (bool): Track gripper height alignment
  
  - Measures vertical (Z-axis) difference between left and right gripper wrists
  - Returns ``bimanual_gripper_vertical_difference`` (lower is better)

**Object Manipulation:**

- ``track_slippage`` (bool): Detect object grip loss
- ``slip_objects`` (list): Props to monitor for slipping
- ``slip_sample_window`` (int): Frames between slip checks (default: 20)
  
  - Detects when gripper loses grip (was holding, now not holding, gripper didn't open)
  - Returns ``slip_count`` and ``slip_count_per_object``

**Safety:**

- ``track_collisions`` (bool): Track collision events
  
  - Detects new collisions with environment and robot self-collisions
  - Returns ``env_collision_count`` and ``self_collision_count``
  - Only counts new collision contacts, not sustained contact

**Trajectory Quality:**

- ``track_cartesian_jerk`` (bool): End-effector smoothness
  
  - Jerk = rate of change of acceleration (derivative of acceleration)
  - Returns ``avg_cartesian_jerk`` and ``rms_cartesian_jerk`` per arm
  - Lower jerk = smoother, more human-like motion

- ``track_joint_jerk`` (bool): Joint space smoothness
  
  - Jerk in joint space
  - Returns ``avg_joint_jerk`` and ``rms_joint_jerk`` per arm

**Efficiency:**

- ``track_cartesian_path_length`` (bool): End-effector path distance
  
  - Total distance traveled by end-effector in cartesian space
  - Returns ``cartesian_path_length`` per arm, ``total_cartesian_path_length``, ``avg_cartesian_path_length``

- ``track_joint_path_length`` (bool): Joint space path distance
  
  - Total distance traveled in joint configuration space
  - Returns ``joint_path_length`` per arm, ``total_joint_path_length``, ``avg_joint_path_length``

- ``track_orientation_path_length`` (bool): Rotation path length
  
  - Total angular distance traveled (quaternion angular distance)
  - Returns ``orientation_path_length`` per arm, ``total_orientation_path_length``

**Required Parameter:**

- ``robot`` (Robot): Robot instance for accessing kinematics and grippers

Metrics Lifecycle
-----------------

**1. Initialize (_metric_init)**

Call in both ``_initialize_env()`` and ``_on_reset()``:

.. code-block:: python

    self._metric_init(
        track_vel_sync=True,
        track_slippage=True,
        slip_objects=[self.cube, self.pot],
        track_collisions=True,
        robot=self.robot,
        slip_sample_window=20
    )
    
    # Initialize stage flags
    for idx in range(1, 4):
        self._metric_stage(idx, False)

**2. Update (_metric_step)**

Call in ``_on_step()`` to update metrics every simulation step:

.. code-block:: python

    def _on_step(self):
        self._metric_step()

This method:

- Tracks velocity and vertical sync differences
- Detects new collisions
- Detects slip events (every N frames based on ``slip_sample_window``)
- Accumulates path lengths
- Calculates and accumulates jerk values

**3. Track Stages (_metric_stage)**

Call during ``_success()`` to mark subtask completion:

.. code-block:: python

    def _success(self):
        # Update stages as task progresses
        if self._is_grasped():
            self._metric_stage(1)  # Stage 1 complete
        
        if self._is_lifted():
            self._metric_stage(2)  # Stage 2 complete
        
        success = self._in_goal_region()
        if success:
            self._metric_stage(3)  # Stage 3 complete
        
        # Finalize...
        return success

**4. Finalize (_metric_finalize)**

Call at end of ``_success()`` to compute final metrics:

.. code-block:: python

    self._final_metrics = self._metric_finalize(
        success_flag=success,
        target_distance={"lift_distance": 0.15, "goal_distance": 0.05},
        pose_error=0.02
    )

Parameters:

- ``success_flag`` (bool): Whether task succeeded
- ``target_distance`` (float or dict): Distance(s) to goal/target
- ``pose_error`` (float or dict): Orientation/pose error(s)

**5. Expose (_get_task_info)**

Return metrics in info dict:

.. code-block:: python

    def _get_task_info(self):
        return getattr(self, "_final_metrics", {})

Metrics Dictionary Structure
-----------------------------

``_metric_finalize()`` returns a comprehensive dictionary:

.. code-block:: python

    metrics = {
        # Core metrics (always present)
        "success": 1.0,  # Float: 1.0 or 0.0
        "completion_time": 15.32,  # Seconds since episode start
        
        # Stage progression (if _metric_stage was called)
        "task_stage_reached": {1: True, 2: True, 3: False},
        "subtask_progress": 0.67,  # 2/3 stages completed
        
        # Custom distances (if target_distance provided)
        "target_distance": {
            "lift_distance": 0.15,
            "goal_distance": 0.05
        },
        # Or single value: "target_distance": 0.05
        
        # Pose errors (if pose_error provided)
        "object_pose_error": 0.02,
        # Or dict: "object_pose_error": {"pot": 0.02, "lid": 0.01}
        
        # Slip tracking (if track_slippage=True)
        "slip_count": 2,  # Total slip events
        "slip_count_per_object": {"object_1": 1, "object_2": 1},
        
        # Collision tracking (if track_collisions=True)
        "env_collision_count": 3,  # New environment collisions
        "self_collision_count": 0,  # Robot self-collisions
        
        # Bimanual coordination (if multiarm and track_vel_sync=True)
        "bimanual_arm_velocity_difference": 0.05,  # Avg velocity diff
        
        # Vertical sync (if multiarm and track_vertical_sync=True)
        "bimanual_gripper_vertical_difference": 0.01,  # Avg height diff
        
        # Path lengths (if track_cartesian_path_length=True)
        "cartesian_path_length": {
            "left": 1.52,
            "right": 1.48
        },
        "total_cartesian_path_length": 3.00,
        "avg_cartesian_path_length": 1.50,
        
        # Joint path (if track_joint_path_length=True)
        "joint_path_length": {
            "left": 8.23,
            "right": 8.45
        },
        "total_joint_path_length": 16.68,
        "avg_joint_path_length": 8.34,
        
        # Orientation path (if track_orientation_path_length=True)
        "orientation_path_length": {
            "left": 0.52,
            "right": 0.48
        },
        "total_orientation_path_length": 1.00,
        "avg_orientation_path_length": 0.50,
        
        # Cartesian jerk (if track_cartesian_jerk=True)
        "avg_cartesian_jerk": {
            "left": 0.32,
            "right": 0.28
        },
        "rms_cartesian_jerk": {
            "left": 0.45,
            "right": 0.41
        },
        "overall_avg_cartesian_jerk": 0.30,
        "overall_rms_cartesian_jerk": 0.43,
        
        # Joint jerk (if track_joint_jerk=True)
        "avg_joint_jerk": {
            "left": 2.1,
            "right": 2.3
        },
        "rms_joint_jerk": {
            "left": 3.2,
            "right": 3.5
        },
        "overall_avg_joint_jerk": 2.2,
        "overall_rms_joint_jerk": 3.35,
    }

**Note:** For single-arm robots, metrics return single values instead of dicts:

.. code-block:: python

    "cartesian_path_length": 1.50,  # Not {"left": 1.50}
    "avg_cartesian_jerk": 0.30,     # Not {"left": 0.30}
---------------

Analyze collected information over episodes:

.. code-block:: python

    import numpy as np
    from typing import Any
    
    # Collect info from multiple episodes
    all_info: list[list[dict[str, Any]]] = []
    
    for episode in range(100):
        obs, info = env.reset()
        episode_info = []
        
        for step in range(1000):
            action = policy.predict(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            
            episode_info.append(info)
            
            if terminated or truncated:
                break
        
        all_info.append(episode_info)
    
    # Compute statistics
    success_rate = np.mean([ep_info[-1]['task_success'] 
                            for ep_info in all_info])
    
    # Analyze custom info if available
    if 'stage' in all_info[0][0]:
        max_stages = [max(step_info['stage'] 
                         for step_info in ep_info)
                      for ep_info in all_info]
        avg_stage = np.mean(max_stages)
        print(f"Average max stage: {avg_stage:.2f}")
    
    print(f"Success rate: {success_rate:.2%}")

    "cartesian_path_length": 1.50,  # Not {"left": 1.50}
    "avg_cartesian_jerk": 0.30,     # Not {"left": 0.30}

Accessing Metrics
-----------------

**During Episode:**

Metrics are only finalized at episode end (when ``_success()`` is called):

.. code-block:: python

    obs, reward, terminated, truncated, info = env.step(action)
    
    if terminated or truncated:
        # Metrics available in info dict
        print(f"Success: {info['success']}")
        print(f"Time: {info['completion_time']:.2f}s")
        print(f"Slips: {info['slip_count']}")
        print(f"Collisions: {info['env_collision_count']}")
        print(f"Progress: {info['subtask_progress']:.1%}")
        
        if 'cartesian_path_length' in info:
            print(f"Path: {info['cartesian_path_length']}")
        
        if 'avg_cartesian_jerk' in info:
            print(f"Jerk: {info['avg_cartesian_jerk']}")

**Collecting Over Episodes:**

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
                # Collect all metrics
                metrics["success"].append(info["success"])
                metrics["completion_time"].append(info["completion_time"])
                metrics["slip_count"].append(info["slip_count"])
                metrics["subtask_progress"].append(info["subtask_progress"])
                
                if "env_collision_count" in info:
                    metrics["collisions"].append(info["env_collision_count"])
                
                if "total_cartesian_path_length" in info:
                    metrics["path_length"].append(info["total_cartesian_path_length"])
                
                if "overall_avg_cartesian_jerk" in info:
                    metrics["jerk"].append(info["overall_avg_cartesian_jerk"])
                
                if "bimanual_arm_velocity_difference" in info:
                    metrics["vel_sync"].append(info["bimanual_arm_velocity_difference"])
                
                break
    
    # Analyze results
    print(f"Success rate: {np.mean(metrics['success']):.2%}")
    print(f"Avg completion time: {np.mean(metrics['completion_time']):.2f}s")
    print(f"Avg slips: {np.mean(metrics['slip_count']):.2f}")
    print(f"Avg collisions: {np.mean(metrics['collisions']):.2f}")
    print(f"Avg subtask progress: {np.mean(metrics['subtask_progress']):.1%}")
    print(f"Avg path length: {np.mean(metrics['path_length']):.3f}")
    print(f"Avg jerk (smoothness): {np.mean(metrics['jerk']):.3f}")
    print(f"Avg velocity sync: {np.mean(metrics['vel_sync']):.3f}")

Interpreting Metrics
--------------------

**Success and Progression:**

- ``success``: Binary task completion (1.0 = success, 0.0 = failure)
- ``subtask_progress``: Percentage of stages completed (0.0 to 1.0)
  
  - Useful for analyzing partial task completion
  - Example: 0.67 = completed 2 out of 3 stages

- ``task_stage_reached``: Which specific stages were reached
  
  - Diagnose where failures occur
  - Example: {1: True, 2: True, 3: False} = grasped and lifted, but failed to place

**Bimanual Coordination:**

- ``bimanual_arm_velocity_difference``: Lower is better
  
  - Measures how synchronized arm movements are
  - High values indicate uncoordinated bimanual manipulation

- ``bimanual_gripper_vertical_difference``: Lower is better
  
  - Measures gripper height alignment
  - Important for tasks requiring level grasping (e.g., carrying trays)

**Manipulation Quality:**

- ``slip_count``: Lower is better (ideally 0)
  
  - Each slip indicates grip failure
  - High slip counts suggest poor grasp quality or excessive forces

- ``slip_count_per_object``: Identifies which objects are problematic
  
  - Example: {"pot": 3, "lid": 0} = pot slips often, lid doesn't

**Safety:**

- ``env_collision_count``: Lower is better (ideally 0)
  
  - Counts new collisions with environment (tables, cabinets, etc.)
  - Does NOT count sustained contact (e.g., gripper on object being manipulated)

- ``self_collision_count``: Should always be 0
  
  - Robot parts colliding with each other
  - Indicates poor motion planning or singularities

**Trajectory Quality:**

- ``avg_cartesian_jerk`` / ``rms_cartesian_jerk``: Lower is better
  
  - Measures motion smoothness
  - Human-like motion has low jerk
  - High jerk = jerky, robotic motion
  - RMS jerk penalizes spikes more than average jerk

- ``avg_joint_jerk`` / ``rms_joint_jerk``: Lower is better
  
  - Joint space smoothness
  - Important for motor wear and energy efficiency

**Efficiency:**

- ``cartesian_path_length``: Lower is better
  
  - Total distance traveled by end-effector
  - Shorter paths = more efficient
  - Compare to ideal/demonstrated path length

- ``joint_path_length``: Lower is better
  
  - Total distance in joint configuration space
  - May differ from cartesian path (redundant arms)

- ``orientation_path_length``: Lower is better
  
  - Total angular distance traveled
  - Excessive rotation indicates inefficient orientation planning

**Custom Metrics:**

- ``target_distance``: Task-specific distance to goal
  
  - Useful for debugging near-misses
  - Can be dict for multiple distances

- ``object_pose_error``: Orientation/pose error
  
  - Measures how close object is to target pose
  - Example: pot upright angle deviation

Adding Custom Metrics
----------------------

You can add task-specific metrics via ``_metric_finalize()`` parameters:

**Distance Metrics:**

.. code-block:: python

    def _success(self):
        cube_pos = self.cube.body.get_position()
        gripper_pos = self.robot.grippers[HandSide.LEFT].wrist_position
        
        # Calculate custom distances
        lift_distance = cube_pos[2] - 1.0  # Height above table
        gripper_distance = np.linalg.norm(cube_pos - gripper_pos)
        goal_distance = np.linalg.norm(cube_pos - self.goal_pos)
        
        success = goal_distance < 0.05
        
        self._final_metrics = self._metric_finalize(
            success_flag=success,
            target_distance={
                "lift_distance": lift_distance,
                "gripper_distance": gripper_distance,
                "goal_distance": goal_distance
            },
            pose_error=0.0
        )
        
        return success

**Pose Error Metrics:**

.. code-block:: python

    def _success(self):
        from pyquaternion import Quaternion
        
        # Calculate orientation error
        pot_quat = Quaternion(self.pot.body.get_quaternion())
        target_quat = Quaternion(axis=[0, 0, 1], angle=0)
        
        # Angular distance between orientations
        angle_error = Quaternion.absolute_distance(pot_quat, target_quat)
        
        success = angle_error < np.deg2rad(10)
        
        self._final_metrics = self._metric_finalize(
            success_flag=success,
            target_distance=0.0,
            pose_error=angle_error  # In radians
        )
        
        return success

**Multiple Object Errors:**

.. code-block:: python

    def _success(self):
        # Track errors for multiple objects
        pose_errors = {}
        
        for obj_name, obj in [("pot", self.pot), ("lid", self.lid)]:
            obj_quat = Quaternion(obj.body.get_quaternion())
            target_quat = self.target_orientations[obj_name]
            pose_errors[obj_name] = Quaternion.absolute_distance(obj_quat, target_quat)
        
        success = all(error < self.threshold for error in pose_errors.values())
        
        self._final_metrics = self._metric_finalize(
            success_flag=success,
            target_distance=0.0,
            pose_error=pose_errors  # Dict of errors
        )
        
        return success

**Accessing Custom Metrics:**

.. code-block:: python

    # These appear in the info dict automatically
    info = env.step(action)[-1]
    
    if "target_distance" in info:
        if isinstance(info["target_distance"], dict):
            for name, dist in info["target_distance"].items():
                print(f"{name}: {dist:.3f}")
        else:
            print(f"Distance: {info['target_distance']:.3f}")
    
    if "object_pose_error" in info:
        if isinstance(info["object_pose_error"], dict):
            for obj, error in info["object_pose_error"].items():
                print(f"{obj} error: {np.rad2deg(error):.1f}°")
        else:
            print(f"Pose error: {np.rad2deg(info['object_pose_error']):.1f}°")

Best Practices
--------------

1. **Always inherit from MetricRolloutEval** - Provides comprehensive, standardized metrics
2. **Initialize metrics in both _initialize_env() and _on_reset()** - Ensures clean state per episode
3. **Call _metric_step() in _on_step()** - Updates metrics every simulation step
4. **Use _metric_stage() for progression tracking** - Helps diagnose where failures occur
5. **Track what's relevant** to your task:
   
   - Slippage for grasping tasks
   - Collisions for safety-critical tasks
   - Velocity/vertical sync for bimanual coordination
   - Jerk for human-like motion
   - Path length for efficiency

6. **Add custom distances and pose errors** - Provides debugging insights beyond binary success
7. **Initialize stage flags** - Set all stages to False in ``_on_reset()`` before tracking
8. **Store and expose metrics properly**:

   .. code-block:: python

       self._final_metrics = self._metric_finalize(...)
       
       def _get_task_info(self):
           return getattr(self, "_final_metrics", {})

9. **Analyze distributions, not just averages** - Use RMS jerk, max slips, 95th percentile path length
10. **Compare against baselines** - Human demonstrations, random policy, previous versions

Common Pitfalls
---------------

**Forgetting to re-initialize in _on_reset():**

.. code-block:: python

    # WRONG - metrics persist across episodes
    def _initialize_env(self):
        self._metric_init(...)
    
    # CORRECT - reset metrics each episode
    def _initialize_env(self):
        self._metric_init(...)
    
    def _on_reset(self):
        self._metric_init(...)  # Re-initialize!

**Not calling _metric_step():**

.. code-block:: python

    # WRONG - metrics never update
    def _on_step(self):
        pass
    
    # CORRECT
    def _on_step(self):
        self._metric_step()

**Accessing metrics before finalization:**

.. code-block:: python

    # WRONG - metrics not available during episode
    obs, reward, terminated, truncated, info = env.step(action)
    print(info['slip_count'])  # May not exist yet!
    
    # CORRECT - only access at episode end
    if terminated or truncated:
        print(info['slip_count'])  # Now available

**Forgetting to store _final_metrics:**

.. code-block:: python

    # WRONG - metrics computed but not stored
    def _success(self):
        self._metric_finalize(...)  # Lost!
        return True
    
    # CORRECT - store in instance variable
    def _success(self):
        self._final_metrics = self._metric_finalize(...)
        return True

See Also
--------

- :doc:`custom-tasks` - Implementing tasks with metrics
- :doc:`../user-guide/demonstrations` - Using metrics with demonstrations
- ``roboeval/utils/metric_rollout.py`` - Full implementation details
- ``roboeval/envs/lift_pot.py`` - Example task using all metrics
