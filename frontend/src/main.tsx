import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";
import "./index.css";

import { ResumeProvider } from "./context/ResumeContext";

ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
).render(
  <React.StrictMode>
    <ResumeProvider>
      <App />
    </ResumeProvider>
  </React.StrictMode>
);