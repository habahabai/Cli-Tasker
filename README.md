# CLI Tasker

A small, single-file-free Python CLI task manager with SQLite persistence.

## Features
- Add, list, complete and delete tasks
- Local SQLite database stored in `~/.tasker/tasks.db` by default
- No external runtime dependencies (standard library only)

## Requirements
- Python 3.8+

## Install / Run
Clone the repo and run directly from the `src` folder, or run the CLI script:

```bash
# run from repo root (uses default DB path ~/.tasker/tasks.db)
python src/tasker/cli.py add "Buy milk" --desc "2 liters"
python src/tasker/cli.py list
```

## Usage
```
# initialize DB manually (optional — CLI will create DB automatically)
python src/tasker/cli.py init-db

# add a task
python src/tasker/cli.py add "Finish report" --desc "by Friday"

# list tasks
python src/tasker/cli.py list
python src/tasker/cli.py list --all

# mark a task done
python src/tasker/cli.py done 1

# delete a task
python src/tasker/cli.py delete 2
```

## Tests
Run the tests with unittest:

```bash
# from repo root
PYTHONPATH=src python -m unittest discover -v
```

## License
MIT
