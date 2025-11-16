RoboEval Documentation Quick Reference
=======================================

## 🚀 Quick Start

### Build Documentation
```bash
cd /home/helen/Documents/projects/bimanual/roboeval-documentation
make html
```

### View Documentation
```bash
# Open in browser
xdg-open _build/html/index.html
# or
firefox _build/html/index.html
```

### Clean Build
```bash
make clean
make html
```

## 📁 Documentation Structure

```
roboeval-documentation/
├── index.rst                          # Main landing page
│
├── getting-started/                   # For new users
│   ├── installation.rst              # Setup & installation
│   ├── quickstart.rst                # Basic examples
│   └── examples.rst                  # Walkthrough of 7 examples
│
├── user-guide/                        # Core concepts
│   ├── environments.rst              # Task environments
│   ├── action-modes.rst              # Robot control modes
│   ├── observations.rst              # Observation configuration
│   ├── data-collection.rst           # Teleop tools
│   └── demonstrations.rst            # Demo dataset
│
├── tasks/                             # Task documentation
│   ├── index.rst                     # Overview of 9 families
│   ├── lift-pot.rst                  # LiftPot (4 variants)
│   ├── stack-books.rst               # Book tasks (7 variants)
│   ├── manipulation.rst              # Basic tasks (9 variants)
│   ├── rotate-valve.rst              # Valve (3 variants)
│   ├── pack-box.rst                  # Packing (4 variants)
│   └── lift-tray.rst                 # Tray (5 variants)
│
├── advanced/                          # Advanced topics
│   ├── custom-tasks.rst              # Create tasks
│   ├── custom-props.rst              # Create objects
│   ├── custom-robots.rst             # Configure robots
│   ├── metrics.rst                   # Evaluation metrics
│   └── integrations.rst              # Framework integration
│
├── api/                               # API reference
│   ├── core.rst                      # RoboEvalEnv
│   ├── environments.rst              # All task classes
│   ├── robots.rst                    # Robot configs
│   ├── demonstrations.rst            # Demo APIs
│   └── utils.rst                     # Utilities
│
├── development/                       # Contributing
│   ├── contributing.rst              # Guidelines
│   └── testing.rst                   # Testing
│
└── _static/                           # Assets
    ├── css/custom.css                # Styling
    └── imgs/                         # Images
```

## 📝 Common Tasks

### Add a New Page
1. Create `.rst` file in appropriate directory
2. Add to `toctree` in parent index
3. Build and verify

### Add Task Documentation
```bash
# Create file
touch tasks/new-task.rst

# Edit tasks/index.rst to add:
# .. toctree::
#    new-task
```

### Add Images
```bash
# Place images in _static/imgs/
cp my_image.png _static/imgs/

# Reference in .rst:
# .. image:: ../_static/imgs/my_image.png
#    :alt: Description
#    :width: 60%
```

### Link to Other Pages
```rst
See :doc:`../user-guide/environments` for details.
See :doc:`quickstart` for examples.
See :ref:`section-label` for specific section.
```

### Code Examples
```rst
.. code-block:: python

    from roboeval.envs.lift_pot import LiftPot
    
    env = LiftPot(...)
    obs, info = env.reset()
```

## 🎨 Customization

### Theme Colors
Edit `_static/css/custom.css`:
```css
h1, h2, h3 {
    color: #your-color;
}
```

### Sphinx Config
Edit `conf.py`:
```python
html_theme_options = {
    "repository_url": "https://github.com/user/repo",
    "use_repository_button": True,
}
```

## 🔍 Verification

### Check Structure
```bash
python verify_docs.py
```

### Check Links
```bash
make linkcheck
```

### Build PDF
```bash
make latexpdf
```

## 📦 What's Included

### Content Coverage
- ✅ Installation & setup
- ✅ Quick start guide
- ✅ 7 example walkthroughs
- ✅ Environment configuration
- ✅ Action modes (joint position, torque)
- ✅ Observation config (cameras, state)
- ✅ Data collection (VR, keyboard)
- ✅ Demo loading & conversion
- ✅ All 9 task families documented
- ✅ 28 task variations
- ✅ Custom task creation guide
- ✅ Custom prop creation
- ✅ Metrics & evaluation
- ✅ Framework integrations
- ✅ Complete API reference
- ✅ Contributing guidelines
- ✅ Testing guidelines

### Features
- 📚 37 documentation files
- 🎯 6 main sections
- 📖 Comprehensive examples
- 🔗 Cross-references
- 💻 Code syntax highlighting
- 🎨 Custom styling
- 🚀 GitHub Actions CI/CD
- 📱 Responsive design

## 🔧 Next Steps

### Before Publishing
1. ✏️ **Replace placeholder images**
   - `_static/imgs/roboeval_overview.png`
   - `_static/imgs/lift_pot.png`
   - Add more task images

2. ✅ **Review content**
   - Check all cross-references
   - Verify code examples
   - Test all links

3. 🎨 **Customize styling**
   - Adjust colors in custom.css
   - Add project branding
   - Configure theme options

4. 📝 **Update metadata**
   - Edit conf.py (authors, version)
   - Update copyright year
   - Verify project info

### Publishing
```bash
# Push to GitHub
git add .
git commit -m "Add RoboEval documentation"
git push origin main

# GitHub Actions will auto-build and deploy
# View at: https://helen9975.github.io/roboeval-documentation/
```

## 📚 Resources

### Sphinx Documentation
- https://www.sphinx-doc.org/
- https://sphinx-book-theme.readthedocs.io/

### reStructuredText
- https://docutils.sourceforge.io/rst.html
- https://www.sphinx-doc.org/en/master/usage/restructuredtext/

### Related
- RoboEval Repo: https://github.com/helen9975/RoboEval
- RoboEval Paper: https://www.arxiv.org/abs/2507.00435
- Taskverse Docs: (reference example)

## 💡 Tips

1. **Build often** - Check changes frequently with `make html`
2. **Use warnings** - Sphinx shows warnings for broken links
3. **Test locally** - Always preview before pushing
4. **Version control** - Commit docs with code changes
5. **Keep organized** - Follow the established structure
6. **Add examples** - Code examples help users understand
7. **Cross-reference** - Link related sections
8. **Update regularly** - Keep docs in sync with code

## ❓ Need Help?

- Check `DOCUMENTATION_SUMMARY.md` for detailed overview
- Run `python verify_docs.py` to verify structure
- See `README.md` for build instructions
- Review existing .rst files for examples
- Consult Sphinx documentation for advanced features

---
**Documentation Version:** 1.0  
**RoboEval Version:** 4.1.0  
**Created:** 2025-01-13
