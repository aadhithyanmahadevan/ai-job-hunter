import type { ButtonHTMLAttributes } from "react";

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
}

export default function Button({
  label,
  ...props
}: Props) {
  return (
    <button
      {...props}
      className="
        px-5
        py-3
        rounded-xl
        bg-cyan-500
        hover:bg-cyan-400
        transition
        font-semibold
        text-white
        cursor-pointer
      "
    >
      {label}
    </button>
  );
}