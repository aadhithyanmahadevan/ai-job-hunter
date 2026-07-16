import Card from "../common/Card";
import { FolderKanban } from "lucide-react";

interface Props {
  projects: string[];
}

export default function ProjectsCard({
  projects,
}: Props) {
  return (
    <Card title="Projects">

      <div className="space-y-4">

        {projects.map((project, index) => (

          <div
            key={index}
            className="
              p-4
              rounded-xl
              bg-slate-800
              border
              border-slate-700
              hover:border-cyan-500
              transition
            "
          >

            <div className="flex items-center gap-3">

              <FolderKanban
                className="text-cyan-400"
                size={20}
              />

              <span className="font-medium">
                {project}
              </span>

            </div>

          </div>

        ))}

      </div>

    </Card>
  );
}