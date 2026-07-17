import {
    Brain,
    Building2,
    ExternalLink,
    MapPin,
    IndianRupee,
    CheckCircle2,
    AlertTriangle,
    Sparkles,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import type { Job } from "../../types";
import useMatch from "../../hooks/useMatch";

interface Props {
    job: Job;
}

export default function JobCard({ job }: Props) {
    const navigate = useNavigate();

    const result = useMatch(job);

    const match = result?.match_score ?? 0;

    const badgeColor = () => {
        if (match >= 85)
            return "bg-green-500 text-white";

        if (match >= 65)
            return "bg-yellow-500 text-black";

        return "bg-red-500 text-white";
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-lg hover:border-cyan-500 hover:shadow-cyan-500/20 transition-all duration-300">

            {/* ---------------- HEADER ---------------- */}

            <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-6">

                <div>

                    <h2 className="text-3xl font-bold text-white">
                        {job.title}
                    </h2>

                    <div className="flex items-center gap-2 mt-4 text-slate-400">
                        <Building2 size={18} />
                        <span>{job.company}</span>
                    </div>

                    <div className="flex items-center gap-2 mt-2 text-slate-400">
                        <MapPin size={18} />
                        <span>{job.location}</span>
                    </div>

                    <div className="flex items-center gap-2 mt-4 text-green-400 font-semibold">

                        <IndianRupee size={18} />

                        <span>
                            {job.salary && job.salary !== "None-None"
                                ? job.salary
                                : "Salary not disclosed"}
                        </span>

                    </div>

                </div>

                <div
                    className={`flex items-center gap-2 px-5 py-3 rounded-full font-bold text-lg ${badgeColor()}`}
                >
                    <Brain size={20} />

                    {match}% Match
                </div>

            </div>

            {/* ---------------- DESCRIPTION ---------------- */}

            <div className="mt-8">

                <h3 className="text-white font-semibold text-lg mb-3">
                    Job Description
                </h3>

                <p className="text-slate-300 leading-8">
                    {job.description.length > 450
                        ? job.description.substring(0, 450) + "..."
                        : job.description}
                </p>

            </div>

            {/* ---------------- REQUIRED SKILLS ---------------- */}

            <div className="mt-8">

                <h3 className="text-white font-semibold text-lg mb-4">
                    Required Skills
                </h3>

                <div className="flex flex-wrap gap-3">

                    {job.skills.length > 0 ? (

                        job.skills.map((skill) => (

                            <span
                                key={skill}
                                className="bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 px-4 py-2 rounded-full text-sm"
                            >
                                {skill}
                            </span>

                        ))

                    ) : (

                        <span className="text-slate-500">
                            Extracting skills...
                        </span>

                    )}

                </div>

            </div>

            {/* ---------------- MATCHED SKILLS ---------------- */}

            {result?.matched_skills.length ? (

                <div className="mt-8">

                    <h3 className="flex items-center gap-2 text-green-400 font-semibold text-lg mb-4">

                        <CheckCircle2 size={20} />

                        Matched Skills

                    </h3>

                    <div className="flex flex-wrap gap-3">

                        {result.matched_skills.map((skill) => (

                            <span
                                key={skill}
                                className="bg-green-500/10 border border-green-500/30 text-green-400 px-4 py-2 rounded-full text-sm"
                            >
                                {skill}
                            </span>

                        ))}

                    </div>

                </div>

            ) : null}

            {/* ---------------- MISSING SKILLS ---------------- */}

            {result?.missing_skills.length ? (

                <div className="mt-8">

                    <h3 className="flex items-center gap-2 text-red-400 font-semibold text-lg mb-4">

                        <AlertTriangle size={20} />

                        Missing Skills

                    </h3>

                    <div className="flex flex-wrap gap-3">

                        {result.missing_skills.map((skill) => (

                            <span
                                key={skill}
                                className="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-2 rounded-full text-sm"
                            >
                                {skill}
                            </span>

                        ))}

                    </div>

                </div>

            ) : null}

            {/* ---------------- AI RECOMMENDATION ---------------- */}

            {result && (

                <div className="mt-8 bg-cyan-500/10 border border-cyan-500/20 rounded-2xl p-5">

                    <div className="flex items-center gap-2 mb-3">

                        <Sparkles
                            className="text-cyan-400"
                            size={20}
                        />

                        <h3 className="text-cyan-400 font-semibold text-lg">
                            AI Recommendation
                        </h3>

                    </div>

                    <p className="text-slate-300 leading-7">
                        {result.recommendation}
                    </p>

                </div>

            )}

            {/* ---------------- FOOTER ---------------- */}

            <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-5 mt-10">

                <span className="text-slate-500 text-sm">
                    Source: {job.source}
                </span>

                <div className="flex gap-3">

                    <button
                        onClick={() =>
                            navigate("/interview", {
                                state: {
                                    job,
                                },
                            })
                        }
                        className="flex items-center gap-2 bg-violet-600 hover:bg-violet-700 px-5 py-3 rounded-xl transition"
                    >
                        <Brain size={18} />

                        Prepare Interview
                    </button>

                    <a
                        href={job.url}
                        target="_blank"
                        rel="noreferrer"
                        className="bg-cyan-500 hover:bg-cyan-400 text-black font-semibold px-5 py-3 rounded-xl transition"
                    >
                        Apply Now
                    </a>

                </div>

            </div>

        </div>
    );
}