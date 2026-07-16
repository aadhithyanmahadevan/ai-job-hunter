import Card from "../common/Card";
import { Award } from "lucide-react";

interface Props {
  certifications: string[];
}

export default function CertificationCard({
  certifications,
}: Props) {

  return (

    <Card title="Certifications">

      <div className="space-y-4">

        {certifications.map((cert, index) => (

          <div
            key={index}
            className="
              flex
              items-center
              gap-3
              p-4
              rounded-xl
              bg-slate-800
              border
              border-slate-700
            "
          >

            <Award
              size={20}
              className="text-yellow-400"
            />

            <span>
              {cert}
            </span>

          </div>

        ))}

      </div>

    </Card>

  );

}