import type { ReactNode } from "react";

interface CardProps {
  title?: string;
  children: ReactNode;
  className?: string;
}

export default function Card({
  title,
  children,
  className = "",
}: CardProps) {
  return (
    <div
      className={`
        rounded-2xl
        border border-slate-800
        bg-slate-900
        shadow-lg
        p-6
        ${className}
      `}
    >
      {title && (
        <h2 className="text-xl font-semibold mb-5 text-white">
          {title}
        </h2>
      )}

      {children}
    </div>
  );
}