// Synthetic fixture; not derived from Supaplate source.
import assert from "node:assert/strict";
import test from "node:test";
import { createTask, search, toggleTask } from "../app/features/tasks/tasks-model.mjs";

const tasks = [
  { id: "one", title: "Write brief", done: false },
  { id: "two", title: "Ship demo", done: true },
];

test("list and filter tasks by q", () => {
  assert.equal(search(tasks, "ship").length, 1);
});

test("create a task without navigation", () => {
  assert.equal(createTask(tasks, "Review").at(-1).title, "Review");
});

test("toggle completion without navigation", () => {
  assert.equal(toggleTask(tasks, "one")[0].done, true);
});
