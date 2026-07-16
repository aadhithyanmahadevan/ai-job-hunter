import type { ReactNode } from "react";
import Card from "../common/Card";

interface StatCardProps {
  title: string;
  value: string | number;
  icon: ReactNode;
  color?: string;
}

export default function StatCard({
  title,
  value,
  icon,
  color = "text-cyan-400",
}: StatCardProps) {
  return (
    <Card className="hover:scale-105 transition-transform duration-300">

      <div className="flex items-center justify-between">

        <div>

          <p className="text-slate-400 text-sm">
            {title}
          </p>

          <h2 className="text-3xl font-bold mt-2">
            {value}
          </h2>

        </div>

        <div className={`text-4xl ${color}`}>
          {icon}
        </div>

      </div>

    </Card>
  );
}