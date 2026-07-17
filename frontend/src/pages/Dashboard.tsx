import StatCard from "../components/dashboard/StatCard";
import ResumeSummary from "../components/dashboard/ResumeSummary";
import SkillsChart from "../components/dashboard/SkillsChart";
import RecentJobs from "../components/dashboard/RecentJobs";

import Card from "../components/common/Card";

import useDashboard from "../hooks/useDashboard";

import {
  FileText,
  Briefcase,
  Award,
  Target,
  Sparkles,
} from "lucide-react";

export default function Dashboard() {

  const {
    resume,
    resumeScore,
    skillsCount,
    projectsCount,
    certificationsCount,
  } = useDashboard();

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
          value={`${resumeScore}%`}
          icon={<FileText />}
        />

        <StatCard
          title="Skills"
          value={skillsCount}
          icon={<Target />}
        />

        <StatCard
          title="Projects"
          value={projectsCount}
          icon={<Briefcase />}
        />

        <StatCard
          title="Certificates"
          value={certificationsCount}
          icon={<Award />}
        />

      </div>

      <div className="grid lg:grid-cols-2 gap-6">

        <Card title="Skill Distribution">
          <SkillsChart />
        </Card>

        <ResumeSummary />

      </div>

      <div className="grid lg:grid-cols-2 gap-6">

        <RecentJobs />

        <Card title="AI Suggestions">

          {resume ? (

            <div className="space-y-4">

              {resume.missing_skills.map((skill: string) => (

                <div
                  key={skill}
                  className="flex items-center gap-3"
                >

                  <Sparkles
                    size={18}
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
              Analyze a resume to get AI suggestions.
            </p>

          )}

        </Card>

      </div>

    </div>

  );

}