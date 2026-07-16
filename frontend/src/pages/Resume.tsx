import { useRef, useState } from "react";

import api from "../services/api";
import { useResume } from "../context/ResumeContext";

import Card from "../components/common/Card";
import Button from "../components/common/Button";

import ProfileCard from "../components/resume/ProfileCard";
import ResumeScore from "../components/resume/ResumeScore";
import SkillsCard from "../components/resume/SkillsCard";
import EducationCard from "../components/resume/EducationCard";
import ProjectsCard from "../components/resume/ProjectsCard";
import CertificationCard from "../components/resume/CertificationCard";
import StrengthCard from "../components/resume/StrengthCard";
import MissingSkillsCard from "../components/resume/MissingSkillsCard";

export default function Resume() {
  const inputRef = useRef<HTMLInputElement>(null);

  const { resume, setResume, clearResume } = useResume();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const chooseFile = () => {
    inputRef.current?.click();
  };

  const analyzeResume = async () => {
    if (!selectedFile) {
      alert("Please choose a resume.");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await api.post(
        "/resume/analyze",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResume(response.data);
    } catch (error) {
      console.error(error);
      alert("Resume analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  const calculateResumeScore = () => {
    if (!resume) return 0;

    let score = 0;

    score += Math.min(resume.skills.length * 2, 40);
    score += Math.min(resume.projects.length * 5, 20);
    score += Math.min(resume.certifications.length * 5, 15);
    score += Math.min(resume.education.length * 10, 10);

    score -= Math.min(resume.missing_skills.length * 2, 15);

    return Math.max(0, Math.min(score, 100));
  };

  return (
    <div className="space-y-8">

      {/* Header */}

      <div className="flex flex-col lg:flex-row justify-between lg:items-center gap-6">

        <div>

          <h1 className="text-5xl font-bold">
            AI Resume Analyzer
          </h1>

          <p className="text-slate-400 mt-3 text-lg">
            Upload your resume and receive an AI-powered technical analysis.
          </p>

        </div>

        {resume && (
          <Button
            label="🔄 Analyze Another Resume"
            onClick={() => {
              clearResume();
              setSelectedFile(null);
            }}
          />
        )}

      </div>

      {/* Upload */}

      {!resume && (

        <Card title="Upload Resume">

          <div className="space-y-8">

            <input
              hidden
              ref={inputRef}
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={(e) => {
                if (
                  e.target.files &&
                  e.target.files.length > 0
                ) {
                  setSelectedFile(e.target.files[0]);
                }
              }}
            />

            {/* File Preview */}

            {selectedFile ? (

              <div className="rounded-2xl border border-cyan-500/30 bg-slate-800 p-5">

                <h3 className="text-cyan-400 font-semibold text-lg">
                  📄 Selected Resume
                </h3>

                <p className="mt-2 text-white">
                  {selectedFile.name}
                </p>

                <p className="text-slate-400 text-sm mt-1">
                  {(selectedFile.size / 1024).toFixed(1)} KB
                </p>

              </div>

            ) : (

              <div className="rounded-2xl border-2 border-dashed border-slate-600 p-10 text-center">

                <h2 className="text-3xl mb-3">
                  📄
                </h2>

                <h3 className="text-xl font-semibold">
                  No Resume Selected
                </h3>

                <p className="text-slate-400 mt-2">
                  Choose a PDF or DOCX resume to begin AI analysis.
                </p>

              </div>

            )}

            {/* Buttons */}

            <div className="flex flex-col md:flex-row gap-5">

              <div className="flex-1">

                <Button
                  label="📂 Choose Resume"
                  onClick={chooseFile}
                />

              </div>

              <div className="flex-1">

                <Button
                  label={
                    loading
                      ? "🤖 Analyzing..."
                      : "🚀 Analyze Resume"
                  }
                  onClick={analyzeResume}
                  disabled={!selectedFile || loading}
                />

              </div>

            </div>

          </div>

        </Card>

      )}

      {/* Resume Report */}

      {resume && (

        <div className="space-y-6">

          <ProfileCard
            name={resume.name}
            title={resume.title}
            experience={resume.years_of_experience}
          />

          <div className="grid lg:grid-cols-2 gap-6">

            <ResumeScore
              score={calculateResumeScore()}
            />

            <EducationCard
              education={resume.education}
            />

          </div>

          <SkillsCard
            skills={resume.skills}
          />

          <div className="grid lg:grid-cols-2 gap-6">

            <ProjectsCard
              projects={resume.projects}
            />

            <CertificationCard
              certifications={resume.certifications}
            />

          </div>

          <div className="grid lg:grid-cols-2 gap-6">

            <StrengthCard
              strengths={resume.strengths}
            />

            <MissingSkillsCard
              missingSkills={resume.missing_skills}
            />

          </div>

        </div>

      )}

    </div>
  );
}