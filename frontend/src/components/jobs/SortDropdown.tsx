interface Props {
  value: string;
  onChange: (value: string) => void;
}

export default function SortDropdown({
  value,
  onChange,
}: Props) {
  return (
    <select
      value={value}
      onChange={(e) =>
        onChange(e.target.value)
      }
      className="bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white"
    >
      <option value="match">
        Highest Match
      </option>

      <option value="company">
        Company
      </option>

      <option value="location">
        Location
      </option>

    </select>
  );
}