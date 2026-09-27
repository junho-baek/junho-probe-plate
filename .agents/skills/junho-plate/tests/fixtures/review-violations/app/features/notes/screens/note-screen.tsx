// Synthetic fixture; not derived from Supaplate source.
import { useEffect, useState } from "react";
import { supabase } from "../../../core/supabase";

export function NoteScreen() {
  const [notes, setNotes] = useState<any[]>([]);

  function NoteRow({ note }: { note: any }) {
    return <li>{note.title}</li>;
  }

  useEffect(() => {
    supabase.from("notes").select("*").then(({ data }) => setNotes(data ?? []));
  }, []);

  return <ul>{notes.map((note: any) => <NoteRow key={note.id} note={note} />)}</ul>;
}
