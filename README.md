# se4sci-project

[![CI](https://github.com/cpappenheimer/se4sci-project/actions/workflows/ci.yml/badge.svg)](https://github.com/cpappenheimer/se4sci-project/actions/workflows/ci.yml)

[API documentation](https://se4sci-project.readthedocs.io)

# Set up
## Install pixi on macOS or Linux
```
curl -fsSL https://pixi.sh/install.sh | bash
# or with brew
brew install pixi
```

# Running the example
First, download the ROOT data file at:  https://drive.google.com/file/d/10Y0m5s1QCeWeGglmDWCwqQoWh7hFuerr/view?usp=sharing
and use the tree name as 'DalitzEventList'
```
pixi run python src/examples/example.py --file <path to ROOT file> --tree-name <name of tree>
```

# Adding a dependency
```
pixi add <dependency>
```

# Running pre-commit
```
pre-commit run -a
```

# Running tests
```
pixi run run_tests
```

# Running tests with log output
```
pixi run run_tests -rP
```

# Preview the documentation locally
```
# Launches the preview at http://localhost:8000/ - use Ctrl-C to quit
pixi run preview_docs
```

# Create visualizations
First, go into `src/graphics_4vecs/plot_4vecs.py` and choose your `filename`, `animation_mode` and `decay_num` to be run.
`filename` should direct to the .csv file generated earlier containing the decay data.

Next, to generate the visualization, run the command:
```
manim -qh <path to plot_4vecs.py> Decay
```
