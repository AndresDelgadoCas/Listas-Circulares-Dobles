# HorseManager

HorseManager is a desktop application for managing a horse stable. It demonstrates a **circular doubly linked list** using Python and a Tkinter graphical interface.

## Features

- Add, update, delete, and search horses.
- Browse horses using **Next** and **Previous**.
- Circular navigation: moving past the last horse returns to the first, and moving before the first returns to the last.
- View registered horses in a table.
- Sample horses are loaded when the application starts.

## Requirements

- Python 3.10 or newer.
- Tkinter (included with most standard Python installations).

No external packages are required.

## Run the application

Open a terminal in this folder and run:

```bash
python main.py
```

On Windows, if `python` is not recognized, try:

```bash
py main.py
```

## Project files

- `main.py`: application entry point.
- `horse.py`: horse data model.
- `circular_doubly_linked_list.py`: node and circular doubly linked list implementation.
- `horse_manager.py`: graphical user interface and event handlers.
- `requirements.txt`: dependency notes.

## Data structure overview

Each node stores a `Horse` object and two references:

- `next`: points to the next node.
- `previous`: points to the previous node.

The last node's `next` points to the head, and the head's `previous` points to the last node. This creates the circular structure in both directions.

## Note

The application keeps records in memory while it is running. Restarting the application restores the sample data.
