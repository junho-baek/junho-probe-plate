// Synthetic fixture; not derived from Supaplate source.
export async function action({ request }: { request: Request }) {
  const formData = await request.formData();
  const title = formData.get("title") as string;
  return { title };
}
