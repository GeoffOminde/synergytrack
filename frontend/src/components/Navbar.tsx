import Link from "next/link";
import { useEffect, useState } from "react";
import { isAuthed, clearToken } from "../lib/auth";

export default function Navbar({ brand = "SynergyTrack" }) {
  ...
  return (
    <nav className="w-full border-b p-3 flex gap-4">
      <Link href="/">{brand}</Link>
      <Link href="/projects">Projects</Link>
      ...
    </nav>
  );
}

