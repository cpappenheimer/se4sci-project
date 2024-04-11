# se4sci-project

# Set up
## Install pixi on macOS or Linux
```
curl -fsSL https://pixi.sh/install.sh | bash
# or with brew
brew install pixi
```

# Running the example
```
pixi run python src/examples/example.py --file <path to input data file> --tree-name <name of tree> --num-events <num events to transform>
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

TODO
