// Synthetic fixture; not derived from Supaplate source.
import { Form } from "react-router";
import { NoteCard } from "../components/note-card";
import type { Note } from "../queries/note.server";

export function NoteScreen({ notes }: { notes: Note[] }) {
  return (
    <main>
      <Form method="post"><input name="title" /><button type="submit">Add</button></Form>
      <ul>{notes.map((note) => <NoteCard key={note.id} title={note.title} />)}</ul>
    </main>
  );
}
