import Card from "../common/Card";
import { CheckCircle2 } from "lucide-react";

interface Props {
  strengths: string[];
}

export default function StrengthCard({
  strengths,
}: Props) {
  return (
    <Card title="Strengths">

      <div className="space-y-3">

        {strengths.map((strength, index) => (

          <div
            key={index}
            className="
              flex
              items-start
              gap-3
              p-4
              rounded-xl
              bg-green-500/10
              border
              border-green-500/30
              hover:bg-green-500/20
              transition-all
              duration-300
            "
          >

            <CheckCircle2
              className="text-green-400 mt-1"
              size={20}
            />

            <span>
              {strength}
            </span>

          </div>

        ))}

      </div>

    </Card>
  );
}