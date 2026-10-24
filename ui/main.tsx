import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";

window.addEventListener("keydown", (e) => {
  if (/^F\d+$/.test(e.key) && !(import.meta.env.DEV && e.key === "F12")) e.preventDefault();
});
if (!import.meta.env.DEV) window.addEventListener("contextmenu", (e) => e.preventDefault());

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
