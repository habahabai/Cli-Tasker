import tempfile
import os
import unittest
from pathlib import Path
from src.tasker.db import TaskDB


class TestTaskDB(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.dbpath = Path(self.tmpdir.name) / "test_tasks.db"
        self.db = TaskDB(self.dbpath)

    def tearDown(self):
        self.db.close()
        self.tmpdir.cleanup()

    def test_add_and_list(self):
        tid = self.db.add_task("Test Task", "Desc")
        self.assertIsInstance(tid, int)
        tasks = self.db.list_tasks()
        self.assertGreaterEqual(len(tasks), 1)
        # newest first: list returns ORDER BY id DESC
        self.assertEqual(tasks[0].title, "Test Task")

    def test_complete_and_delete(self):
        tid = self.db.add_task("To Complete", "")
        ok = self.db.complete_task(tid)
        self.assertTrue(ok)
        task = self.db.get_task(tid)
        self.assertTrue(task.done)
        ok2 = self.db.delete_task(tid)
        self.assertTrue(ok2)


if __name__ == "__main__":
    unittest.main()
