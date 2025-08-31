#!/usr/bin/env python3
"""Simple CLI for Tasker."""
import argparse
import sys
from .db import TaskDB


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tasker", description="Simple CLI task manager")
    sub = parser.add_subparsers(dest="cmd")

    # init-db
    sub.add_parser("init-db", help="Create the database and required folders")

    # add
    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument("--desc", default="", help="Task description")

    # list
    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--all", action="store_true", help="Show all tasks including completed ones")

    # done
    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("task_id", type=int, help="ID of the task to mark done")

    # delete
    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("task_id", type=int, help="ID of the task to delete")

    args = parser.parse_args(argv)

    db = TaskDB()

    if args.cmd == "init-db":
        print(f"Database initialized at: {db.db_path}")
        db.close()
        return 0

    if args.cmd == "add":
        tid = db.add_task(args.title, args.desc)
        print(f"Added task #{tid}: {args.title}")
        db.close()
        return 0

    if args.cmd == "list":
        tasks = db.list_tasks(show_all=args.all)
        if not tasks:
            print("No tasks found.")
            db.close()
            return 0
        for t in tasks:
            status = "✓" if t.done else " "
            print(f"[{status}] {t.id}: {t.title} — {t.description} (created {t.created_at})")
        db.close()
        return 0

    if args.cmd == "done":
        ok = db.complete_task(args.task_id)
        print("Marked done." if ok else "No task found with that ID.")
        db.close()
        return 0

    if args.cmd == "delete":
        ok = db.delete_task(args.task_id)
        print("Deleted." if ok else "No task found with that ID.")
        db.close()
        return 0

    parser.print_help()
    db.close()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
