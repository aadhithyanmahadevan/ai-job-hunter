import { useEffect, useState } from "react";
import { getDashboardData } from "../services/dashboard";

export default function useDashboard() {
  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState<any>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await getDashboardData();
        setDashboard(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return {
    loading,
    dashboard,
  };
}