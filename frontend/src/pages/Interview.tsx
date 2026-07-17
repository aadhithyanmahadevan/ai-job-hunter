import { Navigate, useLocation } from "react-router-dom";
import useInterview from "../hooks/useInterview";
import InterviewHeader from "../components/interview/InterviewHeader";
import TechnicalQuestions from "../components/interview/TechnicalQuestions";
import HRQuestions from "../components/interview/HRQuestions";
import CodingQuestions from "../components/interview/CodingQuestions";

export default function Interview() {
  const location = useLocation();
  const job = location.state?.job;

  if (!job) return <Navigate to="/jobs" replace />;

  const { loading, data } = useInterview(job);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[70vh]">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
          <h2 className="text-2xl font-bold">AI is Preparing Your Interview...</h2>
          <p className="text-slate-400 mt-3">Generating personalized interview questions...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center mt-20">
        <h2 className="text-3xl font-bold text-red-400">Unable to generate interview questions.</h2>
        <p className="text-slate-400 mt-4">Please try again later.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <InterviewHeader job={job} />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h3 className="text-slate-400 mb-2">Interview Readiness</h3>
          <p className="text-4xl font-bold text-green-400">92%</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h3 className="text-slate-400 mb-2">Difficulty</h3>
          <p className="text-4xl font-bold text-yellow-400">Medium</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h3 className="text-slate-400 mb-2">Estimated Time</h3>
          <p className="text-4xl font-bold text-cyan-400">45 min</p>
        </div>
      </div>

      <TechnicalQuestions questions={data.technical} />
      <HRQuestions questions={data.hr} />
      <CodingQuestions topics={data.coding} />

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8">
        <h2 className="text-2xl font-bold mb-6">💡 AI Interview Tips</h2>
        <div className="space-y-4">
          <div className="bg-slate-800 rounded-xl p-4">Review Java Collections and Stream API before your interview.</div>
          <div className="bg-slate-800 rounded-xl p-4">Practice Spring Boot REST API design questions.</div>
          <div className="bg-slate-800 rounded-xl p-4">Revise SQL joins, indexing and query optimization.</div>
          <div className="bg-slate-800 rounded-xl p-4">Be ready to explain one real project end-to-end.</div>
        </div>
      </div>
    </div>
  );
}
