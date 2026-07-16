import Card from "../common/Card";
import { AlertTriangle } from "lucide-react";

interface Props {
  missingSkills: string[];
}

export default function MissingSkillsCard({
  missingSkills,
}: Props) {
  return (
    <Card title="Skills to Learn">

      <div className="flex flex-wrap gap-3">

        {missingSkills.map((skill) => (

          <div
            key={skill}
            className="
              px-4
              py-2
              rounded-full
              bg-red-500/10
              border
              border-red-500/30
              text-red-300
              flex
              items-center
              gap-2
              hover:bg-red-500/20
              transition-all
            "
          >

            <AlertTriangle size={16} />

            {skill}

          </div>

        ))}

      </div>

    </Card>
  );
}