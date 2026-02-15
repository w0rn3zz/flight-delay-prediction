import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Flight Delay Prediction",
  description: "Predict flight delays using ML models",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
