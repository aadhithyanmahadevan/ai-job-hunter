interface Props {
  location: string;
  setLocation: (value: string) => void;
}

export default function FilterBar({
  location,
  setLocation,
}: Props) {
  return (
    <div className="flex gap-4">

      <select
        value={location}
        onChange={(e) =>
          setLocation(e.target.value)
        }
        className="bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white"
      >
        <option value="">All Locations</option>

        <option>Bangalore</option>

        <option>Chennai</option>

        <option>Hyderabad</option>

        <option>Pune</option>

        <option>Remote</option>

      </select>

    </div>
  );
}