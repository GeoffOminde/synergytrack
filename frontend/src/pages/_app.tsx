import type { AppProps } from "next/app";
import "../styles/globals.css";
import Navbar from "../components/Navbar";
import Head from "next/head";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
<Head>
        <title>SynergyTrack</title>
        <meta name="description" content="SynergyTrack — Partnerships for the Goals" />
      </Head>
      <Navbar brand="SynergyTrack" />
      <main className="container mx-auto p-4">
        <Component {...pageProps} />
      </main>
    </>
  );
}
