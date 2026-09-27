// Synthetic fixture; not derived from Supaplate source.
export const supabase = {
  from: (_table: string) => ({
    select: async (_columns: string) => ({ data: [] as unknown[] }),
  }),
};
