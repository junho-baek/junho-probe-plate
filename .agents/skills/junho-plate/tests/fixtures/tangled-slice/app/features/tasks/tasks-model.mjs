// Synthetic fixture; not derived from Supaplate source.
export function search(tasks, query) {
  return tasks.filter((task) => task.title.toLowerCase().includes(query.toLowerCase()));
}

export function createTask(tasks, title) {
  return [...tasks, { id: `synthetic-${tasks.length + 1}`, title, done: false }];
}

export function toggleTask(tasks, id) {
  return tasks.map((task) => task.id === id ? { ...task, done: !task.done } : task);
}
