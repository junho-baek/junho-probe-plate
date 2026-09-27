// Synthetic fixture; not derived from Supaplate source.
import type { NoteInput } from "../schemas/note-schema";

export type Note = { id: string; title: string };

export async function listNotes(): Promise<Note[]> {
  return [{ id: "synthetic-1", title: "A typed note" }];
}

export async function createNote(input: NoteInput): Promise<{ ok: true }> {
  void input;
  return { ok: true };
}
