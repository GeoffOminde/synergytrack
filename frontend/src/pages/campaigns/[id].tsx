import { useRouter } from "next/router";
import useSWR from "swr";
import { api } from "../../lib/api";

export default function CampaignPage() {
  const { query } = useRouter();
  const id = query.id as string;
  const { data: c } = useSWR(id ? `/campaigns/${id}` : null, (p) => api(p));
  if (!c) return <p>Loading...</p>;
  return (
    <div>
      <h2>Campaign #{c.id}</h2>
      <p>Raised {c.amount_raised} / {c.goal_amount} {c.currency}</p>
    </div>
  );
}
