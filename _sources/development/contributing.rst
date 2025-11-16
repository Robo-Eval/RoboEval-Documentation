Contributing
============

We welcome contributions to RoboEval!

Getting Started
---------------

1. **Fork the repository:**

.. code-block:: bash

    git clone https://github.com/helen9975/RoboEval.git
    cd RoboEval

2. **Create a development environment:**

.. code-block:: bash

    conda create -n roboeval-dev python=3.10
    conda activate roboeval-dev
    pip install -e ".[dev]"

3. **Create a feature branch:**

.. code-block:: bash

    git checkout -b feature/my-new-feature

Development Guidelines
----------------------

**Code Style**

We use:

- Black for formatting
- Flake8 for linting
- Type hints where appropriate

Run formatters:

.. code-block:: bash

    black roboeval/
    flake8 roboeval/

**Testing**

Add tests for new features:

.. code-block:: python

    # tests/test_my_feature.py
    import pytest
    from roboeval.envs.my_env import MyEnv
    
    def test_my_feature():
        env = MyEnv(...)
        assert env.some_property == expected_value

Run tests:

.. code-block:: bash

    pytest tests/

**Documentation**

Add docstrings:

.. code-block:: python

    def my_function(param1, param2):
        """Short description.
        
        Longer description of function behavior.
        
        :param param1: Description of param1
        :param param2: Description of param2
        :return: Description of return value
        """
        pass

Contribution Types
------------------

**New Tasks**

1. Create task file in ``roboeval/envs/``
2. Implement required methods
3. Add tests
4. Add documentation
5. Submit PR

**Bug Fixes**

1. Create issue describing bug
2. Fix bug in feature branch
3. Add regression test
4. Submit PR

**Documentation**

1. Improve existing docs
2. Add examples
3. Fix typos
4. Submit PR

Submitting Pull Requests
-------------------------

1. **Ensure tests pass:**

.. code-block:: bash

    pytest tests/
    black roboeval/
    flake8 roboeval/

2. **Write clear commit messages:**

.. code-block:: text

    Add LiftBottle task
    
    - Implements base task and 4 variations
    - Adds tests for success/fail conditions
    - Includes documentation

3. **Submit PR:**

- Reference related issues
- Describe changes
- Include test results

Code Review Process
-------------------

1. Automated tests run on PR
2. Maintainers review code
3. Address feedback
4. Merge when approved

Questions?
----------

- Open an issue on GitHub
- Join our community discussions
- Check existing issues/PRs

See Also
--------

- :doc:`testing` - Testing guidelines
- GitHub repository
