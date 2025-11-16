# RoboEval Documentation

Documentation for the RoboEval bimanual manipulation benchmark.

## Building the Documentation

### Prerequisites

```bash
pip install sphinx sphinx-book-theme
```

### Build HTML

```bash
make html
```

The built documentation will be in `_build/html/`. Open `_build/html/index.html` in your browser.

### Build PDF

```bash
make latexpdf
```

### Clean Build

```bash
make clean
```

## Documentation Structure

```
.
├── index.rst                 # Main index
├── getting-started/          # Installation, quickstart, examples
├── user-guide/              # User guides (environments, actions, etc.)
├── tasks/                   # Task documentation
├── advanced/                # Advanced topics (custom tasks, props, etc.)
├── api/                     # API reference
├── development/             # Contributing, testing
└── _static/                 # Images, CSS, assets
```

## Contributing to Documentation

1. Edit `.rst` files in the appropriate directory
2. Build locally to preview changes: `make html`
3. Submit pull request

### RST Formatting

- Use proper heading levels (=, -, ~, ^)
- Include code examples with syntax highlighting
- Add cross-references with `:doc:` and `:ref:`
- Keep line length reasonable (~80-100 chars)

## Publishing

Documentation is automatically built and published to GitHub Pages on push to main branch via GitHub Actions.

## Local Development

For live reload during development:

```bash
pip install sphinx-autobuild
sphinx-autobuild . _build/html
```

Then open http://127.0.0.1:8000 in your browser.

## Questions?

See the main RoboEval repository: https://github.com/helen9975/RoboEval
