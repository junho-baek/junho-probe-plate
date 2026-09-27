// Synthetic fixture; not derived from Supaplate source.
import { canViewRevenue } from "../../billing/internal/billing-policy";

export function ReportsScreen() {
  return <main>{canViewRevenue("member") ? "Revenue" : "Unavailable"}</main>;
}
