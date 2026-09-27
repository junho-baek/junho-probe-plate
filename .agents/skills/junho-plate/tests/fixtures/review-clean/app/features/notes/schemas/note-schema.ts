// Synthetic fixture; not derived from Supaplate source.
import { z } from "zod";

export const noteSchema = z.object({ title: z.string().trim().min(1).max(120) });
export type NoteInput = z.infer<typeof noteSchema>;
