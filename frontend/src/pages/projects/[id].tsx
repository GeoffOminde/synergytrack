import { useRouter } from "next/router";
import useSWR from "swr";
import { api, API_BASE } from "../../lib/api";
import { useState } from "react";

export default function ProjectDetail() {
  const router = useRouter();
  const id = router.query.id as string;
  const { data: project } = useSWR(id ? `/projects` : null, (p) => api(p));
  const proj = project?.find((x: any) => String(x.id) === id);
  const { data: kpis } = useSWR(id ? `/projects/${id}/kpi` : null, (p) => api(p));
  const [amount, setAmount] = useState(100);

  async function donateMpesa() {
    const phone = prompt("Enter M-Pesa phone (2547XXXXXXXX)");
    await api(`/payments/mpesa/stk?campaign_id=${id}&phone=${phone}&amount=${amount}`, { method: "POST" });
    alert("STK push sent. Complete on your phone.");
  }

  return (
    <div>
      <h2>{proj?.title || "Project"}</h2>
      <p>{proj?.description}</p>
      <h3>KPIs</h3>
      <pre>{JSON.stringify(kpis || [], null, 2)}</pre>
      <h3>Donate</h3>
      <input type="number" value={amount} onChange={e=>setAmount(parseInt(e.target.value || "0"))} />
      <button onClick={donateMpesa}>Donate via M-Pesa</button>
      <a href={`${API_BASE}/ai/nlp/summarize`} style={{ display: "none" }} />
    </div>
  );
}
