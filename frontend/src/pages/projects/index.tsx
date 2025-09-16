import useSWR from "swr";
import { api } from "../../lib/api";
import Link from "next/link";

export default function Projects() {
  const { data, error } = useSWR("/projects", (p) => api(p));
  if (error) return <p>Error loading</p>;
  if (!data) return <p>Loading...</p>;
  return (
    <div>
      <h2>Projects</h2>
      <ul>
        {data.map((p: any) => (
          <li key={p.id}>
            <Link href={`/projects/${p.id}`}>{p.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
