A Python Carpooling problem solver example for using the [CP-SAT Solver](https://developers.google.com/optimization/cp/cp_solver) from Google OR-Tools.

Takes a JSON file with a list of cars and people and returns the optimal carpooling solution.

## Setup

```bash
brew install pdm python@3.12
pdm install
```

### Run the script

```bash
pdm start tests/mocks/one_car.json
```

Or with VSCode, press `F5` and select which mock data to use.

## Running tests

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
