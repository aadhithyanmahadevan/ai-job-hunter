import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  FileText,
  Briefcase,
  Target,
  Download,
  Bot,
} from "lucide-react";

const menuItems = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
    path: "/",
  },
  {
    name: "Resume",
    icon: FileText,
    path: "/resume",
  },
  {
    name: "Jobs",
    icon: Briefcase,
    path: "/jobs",
  },
  {
    name: "AI Match",
    icon: Target,
    path: "/match",
  },
  {
    name: "Export",
    icon: Download,
    path: "/export",
  },
];

export default function Sidebar() {
  return (
    <aside className="w-72 bg-slate-900 border-r border-slate-800 flex flex-col">

      {/* Logo */}

      <div className="h-20 flex items-center justify-center border-b border-slate-800">

        <div className="flex items-center gap-3">

          <Bot size={34} className="text-cyan-400" />

          <div>

            <h1 className="font-bold text-xl">
              AI Job Hunter
            </h1>

            <p className="text-xs text-slate-400">
              Powered by Gemini
            </p>

          </div>

        </div>

      </div>

      {/* Navigation */}

      <nav className="flex-1 px-5 py-8">

        <ul className="space-y-3">

          {menuItems.map((item) => {

            const Icon = item.icon;

            return (

              <li key={item.name}>

                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300
                    ${
                      isActive
                        ? "bg-cyan-500 text-white shadow-lg"
                        : "text-slate-300 hover:bg-slate-800 hover:text-white"
                    }`
                  }
                >

                  <Icon size={22} />

                  <span className="font-medium">
                    {item.name}
                  </span>

                </NavLink>

              </li>

            );

          })}

        </ul>

      </nav>

      {/* Footer */}

      <div className="p-5 border-t border-slate-800">

        <div className="rounded-xl bg-slate-800 p-4">

          <h3 className="font-semibold text-cyan-400">
            AI Assistant
          </h3>

          <p className="text-sm text-slate-400 mt-2">
            Analyze resumes, match jobs and prepare interviews.
          </p>

        </div>

      </div>

    </aside>
  );
}