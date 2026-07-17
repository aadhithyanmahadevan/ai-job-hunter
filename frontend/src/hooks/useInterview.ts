import { useEffect, useState } from "react";
import { getInterviewQuestions } from "../services/interview";

export interface InterviewResult {
  technical: string[];
  hr: string[];
  coding: string[];
}

export default function useInterview(job: any) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<InterviewResult | null>(null);

  useEffect(() => {
    async function load() {
      if (!job) {
        setLoading(false);
        return;
      }

      try {
        const response = await getInterviewQuestions(job.description);

        if (response.success) {
          setData(response.data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [job]);

  return {
    loading,
    data,
  };
}