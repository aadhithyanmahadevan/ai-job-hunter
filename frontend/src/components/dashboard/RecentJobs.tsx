import Card from "../common/Card";

const jobs = [
    "Google",
    "Microsoft",
    "JPMorgan",
    "Amazon",
];

export default function RecentJobs() {

    return (

        <Card title="Recent Jobs">

            <div className="space-y-3">

                {jobs.map((job) => (

                    <div
                        key={job}
                        className="border-b border-slate-700 pb-3"
                    >
                        {job}
                    </div>

                ))}

            </div>

        </Card>

    );

}