// Synthetic fixture; not derived from Supaplate source.
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

test("dashboard route keeps its screen seam", async () => {
  const source = await readFile(new URL("../app/routes/dashboard.tsx", import.meta.url), "utf8");
  assert.match(source, /DashboardScreen/);
});
