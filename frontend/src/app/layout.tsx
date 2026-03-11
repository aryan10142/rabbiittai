import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sales Insight Automator",
  description:
    "Upload sales data and receive an AI-generated executive summary via email.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-950 text-gray-100 antialiased">
        {children}
      </body>
    </html>
  );
}
