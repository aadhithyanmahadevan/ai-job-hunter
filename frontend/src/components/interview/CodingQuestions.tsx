interface Props {
  topics: string[];
}

export default function CodingQuestions({
  topics,
}: Props) {

  return (

    <div className="bg-slate-900 rounded-2xl border border-slate-800 p-8">

      <h2 className="text-2xl font-bold mb-6">
        🧩 Coding Topics
      </h2>

      <div className="flex flex-wrap gap-3">

        {topics.map((topic) => (

          <span
            key={topic}
            className="bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-4 py-2 rounded-full"
          >
            {topic}
          </span>

        ))}

      </div>

    </div>

  );

}