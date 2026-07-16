import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";

/*
|--------------------------------------------------------------------------
| Resume Analysis Model
|--------------------------------------------------------------------------
*/

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

/*
|--------------------------------------------------------------------------
| Context Type
|--------------------------------------------------------------------------
*/

interface ResumeContextType {
  resume: ResumeAnalysis | null;

  setResume: (
    resume: ResumeAnalysis | null
  ) => void;

  clearResume: () => void;
}

/*
|--------------------------------------------------------------------------
| Context
|--------------------------------------------------------------------------
*/

const ResumeContext = createContext<
  ResumeContextType | undefined
>(undefined);

/*
|--------------------------------------------------------------------------
| Provider
|--------------------------------------------------------------------------
*/

export function ResumeProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [resume, setResume] =
    useState<ResumeAnalysis | null>(null);

  const clearResume = () => {
    setResume(null);
  };

  return (
    <ResumeContext.Provider
      value={{
        resume,
        setResume,
        clearResume,
      }}
    >
      {children}
    </ResumeContext.Provider>
  );
}

/*
|--------------------------------------------------------------------------
| Hook
|--------------------------------------------------------------------------
*/

export function useResume() {
  const context = useContext(ResumeContext);

  if (!context) {
    throw new Error(
      "useResume must be used inside ResumeProvider"
    );
  }

  return context;
}