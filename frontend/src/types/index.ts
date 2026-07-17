export interface ResumeAnalysis {
  name: string;
  title: string;
  years_of_experience: string;

  skills: string[];

  education: string[];

  certifications: string[];

  projects: string[];

  strengths: string[];

  missing_skills: string[];
}

export interface DashboardSummary {
  resumeScore: number;

  skills: number;

  projects: number;

  certifications: number;

  strengths: string[];

  missingSkills: string[];

  resume: ResumeAnalysis | null;
}

export interface Job {
  title: string;
  company: string;
  location: string;
  description: string;
  salary: string;
  url: string;
  source: string;
  skills: string[];
}

export interface MatchResult {
  job_title: string;
  company: string;
  match_score: number;
  missing_skills: string[];
  strengths: string[];
  recommendation: string;
}
