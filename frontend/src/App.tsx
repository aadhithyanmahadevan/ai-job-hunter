import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Resume from "./pages/Resume";
import Jobs from "./pages/Jobs";
import Match from "./pages/Match";
import Interview from "./pages/Interview";


function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-slate-950 text-white">
        <Sidebar />

        <div className="flex-1 flex flex-col">
          <Navbar />

          <main className="flex-1 overflow-y-auto p-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/resume" element={<Resume />} />
              <Route path="/jobs" element={<Jobs />} />
              <Route path="/match" element={<Match />} />
              <Route path="/interview" element={<Interview />}
              />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;