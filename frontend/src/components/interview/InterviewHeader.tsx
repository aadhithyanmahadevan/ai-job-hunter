interface Props {
  job: any;
}

export default function InterviewHeader({
  job,
}: Props) {
  return (
    <div className="bg-slate-900 rounded-2xl border border-slate-800 p-8">

      <h1 className="text-4xl font-bold">
        {job.title}
      </h1>

      <p className="text-cyan-400 mt-2 text-xl">
        {job.company}
      </p>

      <p className="text-slate-400 mt-2">
        📍 {job.location}
      </p>

    </div>
  );
}