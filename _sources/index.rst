Welcome to RoboEval's Documentation
====================================

.. image:: _static/imgs/roboeval_overview.png
   :alt: RoboEval Overview
   :align: center
   :width: 80%

**RoboEval** is a structured benchmark for bimanual robotic manipulation that provides:

- **8 task families** with **28 total variations**
- **3,000+ human-collected demonstrations** via VR and keyboard teleoperation
- **Rich diagnostic metrics** beyond binary success (coordination, efficiency, safety, task progression)
- **Standardized tools** for data collection, conversion, and evaluation

Read our paper: `RoboEval: Where Robotic Manipulation Meets Structured and Scalable Evaluation <https://www.arxiv.org/abs/2507.00435>`_

Key Features
------------

**Diverse Bimanual Tasks**
   From basic manipulation (StackTwoBlocks) to complex coordination (LiftPot, PackBox)

**Comprehensive Metrics**
   Track task progression, coordination quality, trajectory efficiency, and spatial proximity

**Flexible Data Collection**
   VR teleoperation (Oculus Quest) and keyboard control for high-quality demonstrations

**Easy Integration**
   Built on Gymnasium API with support for multiple action modes and observation configs

**Extensible**
   Add custom tasks, props, robots, and metrics with well-documented APIs

Quick Start
-----------

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPot
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.robots.configs.panda import BimanualPanda
    
    env = LiftPot(
        action_mode=JointPositionActionMode(),
        render_mode="human",
        robot_cls=BimanualPanda
    )
    
    obs, info = env.reset()
    for _ in range(1000):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            break

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting-started/installation
   getting-started/quickstart
   getting-started/examples

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user-guide/environments
   user-guide/action-modes
   user-guide/observations
   user-guide/data-collection
   user-guide/demonstrations

.. toctree::
   :maxdepth: 2
   :caption: Tasks & Environments

   tasks/index
   tasks/lift-pot
   tasks/stack-books
   tasks/manipulation
   tasks/rotate-valve
   tasks/pack-box
   tasks/lift-tray

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   advanced/custom-tasks
   advanced/custom-props
   advanced/custom-robots
   advanced/metrics

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/core
   api/environments
   api/robots
   api/demonstrations
   api/utils

.. toctree::
   :maxdepth: 1
   :caption: Development

   development/contributing
   development/testing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
