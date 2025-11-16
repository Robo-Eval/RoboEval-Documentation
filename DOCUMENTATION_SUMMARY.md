RoboEval Documentation Summary
==============================

This document provides an overview of the complete RoboEval documentation structure.

## Documentation Structure

### 1. Getting Started
- **installation.rst** - Installation guide with prerequisites, setup steps, and troubleshooting
- **quickstart.rst** - Quick start guide with basic examples and common patterns
- **examples.rst** - Detailed walkthrough of all 7 example scripts

### 2. User Guide
- **environments.rst** - Overview of all task environments, parameters, and configuration
- **action-modes.rst** - Comprehensive guide to action modes (joint position, torque, delta)
- **observations.rst** - Configuration guide for observations and camera setup
- **data-collection.rst** - Tools for keyboard and VR teleoperation
- **demonstrations.rst** - Working with demonstration dataset, replay, and conversion

### 3. Tasks & Environments
- **index.rst** - Overview of all 9 task families with 28 variations
- **lift-pot.rst** - Detailed LiftPot task documentation (4 variations)
- **stack-books.rst** - Book stacking tasks (7 variations)
- **manipulation.rst** - Basic manipulation tasks (9 variations)
- **rotate-valve.rst** - Valve rotation task (3 variations)
- **pack-box.rst** - Box packing task (4 variations)
- **lift-tray.rst** - Tray lifting tasks (5 variations)

### 4. Advanced Topics
- **custom-tasks.rst** - Complete guide to creating custom manipulation tasks
- **custom-props.rst** - Creating custom objects/props for environments
- **custom-robots.rst** - Configuring and adding custom robot configurations
- **metrics.rst** - Understanding and implementing custom metrics
- **integrations.rst** - Integration with LeRobot, RLDS, OpenVLA, and custom frameworks

### 5. API Reference
- **core.rst** - Core RoboEvalEnv class documentation
- **environments.rst** - All environment class references
- **robots.rst** - Robot configuration APIs
- **demonstrations.rst** - Demo loading, saving, conversion APIs
- **utils.rst** - Utility classes (ObservationConfig, MetricRollout, etc.)

### 6. Development
- **contributing.rst** - Contribution guidelines and workflow
- **testing.rst** - Testing guidelines and best practices

## Key Features Documented

### Comprehensive Task Coverage
- 9 task families: LiftPot, StackBooks, Manipulation, RotateValve, PackBox, LiftTray
- 28 total variations with position and orientation randomization
- Progressive difficulty levels from easy to hard
- Task progression stages for fine-grained evaluation

### Flexible Control
- Multiple action modes: absolute/delta joint positions, torque control
- Floating base support for mobile robots
- Configurable control frequencies (20-500 Hz)
- Gripper control integration

### Rich Observations
- Robot state (joint positions, velocities, forces)
- Multi-camera support with RGB and depth
- Configurable camera positions and resolutions
- Custom observation spaces

### Data Collection Tools
- Keyboard teleoperation with customizable controls
- VR teleoperation with Oculus Quest support
- Demonstration recording and replay
- Multiple data format conversions (LeRobot, RLDS)

### Evaluation & Metrics
- Beyond binary success: task progression, coordination, efficiency
- Stage-based evaluation for partial success
- Metrics collection over multiple episodes
- Integration with learning frameworks

## Documentation Highlights

### For New Users
1. Start with **getting-started/installation.rst**
2. Follow **getting-started/quickstart.rst** 
3. Try examples in **getting-started/examples.rst**
4. Explore specific tasks in **tasks/** directory

### For Researchers
1. Review **tasks/index.rst** for task overview
2. Check **user-guide/environments.rst** for configuration
3. See **user-guide/demonstrations.rst** for dataset usage
4. Read **advanced/metrics.rst** for evaluation details

### For Developers
1. Study **advanced/custom-tasks.rst** for task creation
2. Review **api/** directory for class references
3. Check **development/contributing.rst** for guidelines
4. See **development/testing.rst** for testing

### For Integration
1. Check **advanced/integrations.rst** for framework integration
2. See **api/demonstrations.rst** for data conversion
3. Review examples 2-4 for practical integration patterns

## Building the Documentation

```bash
# Install dependencies
pip install sphinx sphinx-book-theme

# Build HTML
make html

# View locally
open _build/html/index.html

# Build PDF (requires LaTeX)
make latexpdf

# Clean build
make clean
```

## Customization Points

### Images
Replace placeholder images in `_static/imgs/`:
- `roboeval_overview.png` - Main overview image (1200x600)
- `lift_pot.png` - Task visualization images (800x600)
- Add more task images as needed

### Styling
Customize in `_static/css/custom.css`:
- Colors and fonts
- Task card styling
- Code block formatting

### Configuration
Modify `conf.py`:
- Theme options
- Extensions
- Project metadata
- Intersphinx mappings

## Publishing

Documentation auto-publishes to GitHub Pages via `.github/workflows/deploy-docs.yml` on push to main.

## TODO / Future Enhancements

1. **Add actual task images** - Replace placeholder images with screenshots
2. **Video tutorials** - Add embedded videos for complex tasks
3. **Interactive examples** - Add Jupyter notebook examples
4. **Performance guide** - Add section on optimization and performance
5. **FAQ section** - Common questions and troubleshooting
6. **Glossary** - Define technical terms
7. **Bibliography** - Add references to related papers

## Key Differences from Taskverse Documentation

This RoboEval documentation:
1. **Focuses on bimanual manipulation** vs general tasks
2. **Emphasizes data collection tools** (VR, keyboard teleop)
3. **Highlights demonstration dataset** (3000+ demos)
4. **Documents rich metrics** beyond success/failure
5. **Includes integration guides** for learning frameworks
6. **Provides robot configuration** (BimanualPanda vs H1)
7. **Details task variations** (position/orientation randomization)

## Contact & Support

- GitHub: https://github.com/helen9975/RoboEval
- Paper: https://www.arxiv.org/abs/2507.00435
- Issues: Use GitHub issue tracker
- Docs Issues: Report in documentation repository

## Version

Documentation Version: 1.0
RoboEval Version: 4.1.0
Last Updated: 2025-01-13
