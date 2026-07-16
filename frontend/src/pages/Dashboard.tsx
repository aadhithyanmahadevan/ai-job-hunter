import { useResume } from "../context/ResumeContext";

import StatCard from "../components/dashboard/StatCard";
import SkillsChart from "../components/dashboard/SkillsChart";
import ResumeSummary from "../components/dashboard/ResumeSummary";
import RecentJobs from "../components/dashboard/RecentJobs";

import Card from "../components/common/Card";

import {
  FileText,
  Briefcase,
  Target,
  Award,
  Sparkles,
} from "lucide-react";

export default function Dashboard() {
  const { resume } = useResume();

  const calculateResumeScore = () => {
    if (!resume) return 0;

    let score = 0;

    score += Math.min(resume.skills.length * 2, 40);
    score += Math.min(resume.projects.length * 5, 20);
    score += Math.min(
      resume.certifications.length * 5,
      15
    );
    score += Math.min(
      resume.education.length * 10,
      10
    );
    score -= Math.min(
      resume.missing_skills.length * 2,
      15
    );

    return Math.max(0, Math.min(score, 100));
  };

  return (
    <div className="space-y-8">

      <div>

        <h1 className="text-4xl font-bold">
          Dashboard
        </h1>

        <p className="text-slate-400 mt-2">
          Welcome back! Here's your AI career overview.
        </p>

      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        <StatCard
          title="Resume Score"
          value={
            resume
              ? `${calculateResumeScore()}%`
              : "--"
          }
          icon={<FileText />}
        />

        <StatCard
          title="Skills"
          value={
            resume
              ? resume.skills.length
              : "--"
          }
          icon={<Target />}
        />

        <StatCard
          title="Projects"
          value={
            resume
              ? resume.projects.length
              : "--"
          }
          icon={<Briefcase />}
        />

        <StatCard
          title="Certifications"
          value={
            resume
              ? resume.certifications.length
              : "--"
          }
          icon={<Award />}
        />

      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        <Card title="Skill Distribution">

          <SkillsChart />

        </Card>

        <ResumeSummary />

        <RecentJobs />

        <Card title="AI Suggestions">

          {resume ? (

            <div className="space-y-4">

              {resume.missing_skills.map((skill) => (

                <div
                  key={skill}
                  className="flex items-center gap-3"
                >

                  <Sparkles
                    size={20}
                    className="text-cyan-400"
                  />

                  <span>
                    Learn {skill}
                  </span>

                </div>

              ))}

            </div>

          ) : (

            <p className="text-slate-400">
              Analyze your resume to get AI suggestions.
            </p>

          )}

        </Card>

      </div>

    </div>
  );
}