A Python Carpooling problem solver example for using the [CP-SAT Solver](https://developers.google.com/optimization/cp/cp_solver) from [Google OR-Tools](https://developers.google.com/optimization/introduction/python).

Takes a JSON file with a list of cars and people and returns the optimal carpooling solution.

### Setup

```bash
brew install pdm python@3.12
pdm install
```

### Run the script

```bash
pdm start tests/mocks/one_car.json
```

Or with VSCode, press <kbd>F5</kbd> and select which mock data to use.

### Running tests

```bash
pdm test
```

Run a specific test:

```bash
pdm test -k "test_name_pattern"
```

Run tests with debug logs:

```bash
pdm test_logs
```

Run tests in watch mode:

```bash
pdm test_watch # Run tests in watch mode
```
