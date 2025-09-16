import { useState } from "react";
import { API_BASE } from "../lib/api";
import { saveToken } from "../lib/auth";

export default function Login() {
  const [email, setEmail] = useState(""); const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setError(null);
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) { setError("Invalid credentials"); return; }
    const data = await res.json();
    saveToken(data.access_token);
    location.href = "/projects";
  }

  return (
    <div style={{ maxWidth: 380 }}>
      <h2>Sign in</h2>
      <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button onClick={submit}>Login</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
