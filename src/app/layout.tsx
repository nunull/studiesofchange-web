import type { Metadata } from "next";
import "./globals.css";


export const metadata: Metadata = {
  title: `Studies of Change`,
  description: `Studies of Change will be an exhibition by 26 artists from the Hochschule für Künste Bremen that links art with technological, social, ecological, and political realms.
  From 29th May to 2nd June 2024 it will open the doors of Bremen’s Alte Pathologie to offer new ways of looking at the former municipal site.`,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="favicon/apple-touch-icon.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="favicon/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="favicon/favicon-16x16.png"
        />
        <link rel="manifest" href="favicon/site.webmanifest" />
        <link
          rel="mask-icon"
          href="favicon/safari-pinned-tab.svg"
          color="#000000"
        />
        <link rel="shortcut icon" href="favicon/favicon.ico" />
        <meta name="msapplication-TileColor" content="#000000" />
        <meta
          name="msapplication-config"
          content="favicon/browserconfig.xml"
        />
        <meta name="theme-color" content="#000" />
      </head>
      <body className="font-sans">
        <div className="min-h-screen">{children}</div>
        {/* <Footer /> */}
      </body>
    </html>
  );
}