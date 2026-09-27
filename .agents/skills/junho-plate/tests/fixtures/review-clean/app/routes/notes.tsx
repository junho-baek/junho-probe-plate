// Synthetic fixture; not derived from Supaplate source.
import { NoteScreen } from "../features/notes";
import { createNote, listNotes } from "../features/notes/queries/note.server";
import { noteSchema } from "../features/notes/schemas/note-schema";

export async function loader() {
  return { notes: await listNotes() };
}

export async function action({ request }: { request: Request }) {
  const input = noteSchema.parse(Object.fromEntries(await request.formData()));
  return createNote(input);
}

export default function NotesRoute({ loaderData }: { loaderData: Awaited<ReturnType<typeof loader>> }) {
  return <NoteScreen notes={loaderData.notes} />;
}
