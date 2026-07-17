interface Props {
  questions: string[];
}

export default function TechnicalQuestions({
  questions,
}: Props) {

  return (

    <div className="bg-slate-900 rounded-2xl border border-slate-800 p-8">

      <h2 className="text-2xl font-bold mb-6">
        💻 Technical Questions
      </h2>

      <div className="space-y-4">

        {questions.map((question, index) => (

          <div
            key={index}
            className="bg-slate-800 rounded-xl p-4"
          >

            <p>

              <span className="text-cyan-400 font-bold">
                Q{index + 1}.
              </span>{" "}

              {question}

            </p>

          </div>

        ))}

      </div>

    </div>

  );

}