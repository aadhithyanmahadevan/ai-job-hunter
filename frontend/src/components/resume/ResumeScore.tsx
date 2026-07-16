import Card from "../common/Card";

interface Props {
    score: number;
}

export default function ResumeScore({
    score,
}: Props) {

    const color =
        score >= 85
            ? "text-green-400"
            : score >= 70
                ? "text-yellow-400"
                : "text-red-400";

    const progressColor =
        score >= 85
            ? "bg-green-500"
            : score >= 70
                ? "bg-yellow-500"
                : "bg-red-500";

    return (

        <Card title="Resume Score">

            <div className="space-y-6">

                <div className="text-center">

                    <h1
                        className={`text-6xl font-bold ${color}`}
                    >

                        {score}%

                    </h1>

                    <p className="text-slate-400 mt-2">

                        AI Confidence Score

                    </p>

                </div>

                <div
                    className="
                    w-full
                    h-4
                    rounded-full
                    bg-slate-700
                    overflow-hidden
                "
                >

                    <div
                        className={`h-full ${progressColor}`}
                        style={{
                            width: `${score}%`,
                        }}
                    />

                </div>

                <div className="flex justify-between text-sm text-slate-400">

                    <span>

                        Needs Improvement

                    </span>

                    <span>

                        Excellent

                    </span>

                </div>

            </div>

        </Card>

    );

}