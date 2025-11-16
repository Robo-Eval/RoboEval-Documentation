Installation
============

Prerequisites
-------------

- Python 3.10+
- Git with submodule support
- (Optional) CUDA-compatible GPU for model evaluation
- (Optional) Oculus Quest for VR teleoperation

System Requirements
-------------------

**Operating Systems:**

- Linux (Ubuntu 20.04+ recommended)
- macOS (with some limitations on rendering)
- Windows (with WSL2)

**Dependencies:**

- MuJoCo 3.1.5
- Gymnasium
- NumPy 1.26.x
- PyTorch (for model evaluation)

Quick Installation
------------------

1. **Clone the repository with submodules:**

.. code-block:: bash

    git clone --recurse-submodules https://github.com/helen9975/RoboEval.git
    cd RoboEval

If you already cloned without submodules:

.. code-block:: bash

    git submodule update --init --recursive

2. **Create and activate conda environment:**

.. code-block:: bash

    conda create -n roboeval python=3.10 -y
    conda activate roboeval

3. **Install the package:**

Choose the installation option that fits your needs:

.. code-block:: bash

    # Core package only
    pip install -e .

    # With example scripts (recommended for first-time users)
    pip install -e ".[examples]"

    # With VR teleoperation support
    pip install -e ".[vr]"

    # Development installation (includes testing and linting tools)
    pip install -e ".[dev]"

    # All features
    pip install -e ".[examples,vr,dev]"

Installation Options Explained
-------------------------------

**Core Installation** (``pip install -e .``)
   Includes only the essential dependencies to run environments and replay demonstrations.

**Examples** (``.[examples]``)
   Adds dependencies for running example scripts including model evaluation (OpenVLA, ACT, etc.)

**VR Support** (``.[vr]``)
   Adds PyOpenXR and related dependencies for Oculus Quest teleoperation.

**Development** (``.[dev]``)
   Includes pytest, black, flake8, and other development tools.

Verify Installation
-------------------

Test your installation by running a simple demo replay:

.. code-block:: bash

    python examples/1_data_replay.py

This script will:

1. Download demonstration data (on first run)
2. Initialize the environment
3. Replay recorded demonstrations

You should see a MuJoCo viewer window showing a bimanual robot replaying a task.

Troubleshooting
---------------

**MuJoCo rendering issues**

If you encounter OpenGL or rendering errors:

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt-get install libgl1-mesa-dev libegl1-mesa-dev

    # Also try setting:
    export MUJOCO_GL=egl

**Missing system libraries**

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt-get install build-essential libglfw3 libglfw3-dev

**CUDA/GPU issues**

For model evaluation, ensure CUDA is properly installed:

.. code-block:: bash

    # Check CUDA availability
    python -c "import torch; print(torch.cuda.is_available())"

**Submodule issues**

If you see import errors related to ``mujoco_menagerie`` or ``mojo``:

.. code-block:: bash

    git submodule update --init --recursive

Next Steps
----------

- Follow the :doc:`quickstart` guide to run your first environment
- Explore :doc:`examples` to learn about data collection and evaluation
- Read about :doc:`../user-guide/environments` to understand task variations
