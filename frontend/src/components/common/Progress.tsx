interface Props {
  value: number;
}

export default function Progress({
  value,
}: Props) {
  return (
    <div className="w-full bg-slate-800 rounded-full h-3">

      <div
        className="bg-cyan-500 h-3 rounded-full transition-all duration-500"
        style={{
          width: `${value}%`,
        }}
      />

    </div>
  );
}