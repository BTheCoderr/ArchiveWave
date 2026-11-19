import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "ArchiveWave | Podcast Archive Intelligence", description: "Find outdated sponsor reads and prepare your podcast archive for fresh ad opportunities." };
export default function RootLayout({children}:{children:React.ReactNode}) {return <html lang="en"><body>{children}</body></html>}