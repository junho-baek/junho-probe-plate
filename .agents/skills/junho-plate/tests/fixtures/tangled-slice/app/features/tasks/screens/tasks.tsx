// Synthetic fixture; not derived from Supaplate source.
import { useEffect, useState } from "react";
import { supabase } from "../../../core/supabase/browser";
import { createTask, search, toggleTask } from "../tasks-model.mjs";

type RawTaskJoin = { id: string; title: string; done: boolean; profiles: { display_name: string }[] };

export function TasksScreen() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [query, setQuery] = useState("");

  function TaskRow({ task }: { task: RawTaskJoin }) {
    return <button onClick={() => setTasks(toggleTask(tasks, task.id))}>{task.title}</button>;
  }

  useEffect(() => {
    supabase.from("tasks").select().then(({ data }) => setTasks(data));
  }, []);

  async function submit(title: string) {
    await fetch("/tasks", { method: "POST", body: JSON.stringify({ title }) });
    setTasks(createTask(tasks, title));
  }

  return <main><input value={query} onChange={(event) => setQuery(event.target.value)} /><button onClick={() => submit("New task")}>Create</button>{search(tasks, query).map((task: any) => <TaskRow key={task.id} task={task} />)}</main>;
}
