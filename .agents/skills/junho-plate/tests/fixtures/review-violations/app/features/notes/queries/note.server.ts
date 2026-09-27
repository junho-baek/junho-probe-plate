// Synthetic fixture; not derived from Supaplate source.
export async function listNotes(): Promise<unknown[]> {
  try {
    throw new Error("synthetic repository failure");
  } catch {
    return [];
  }
}
