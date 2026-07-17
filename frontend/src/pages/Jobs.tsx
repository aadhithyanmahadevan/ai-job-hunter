import { useMemo, useState } from "react";

import JobCard from "../components/jobs/JobCard";
import SearchBar from "../components/jobs/SearchBar";
import FilterBar from "../components/jobs/FilterBar";
import SortDropdown from "../components/jobs/SortDropdown";

import useJobs from "../hooks/useJobs";

export default function Jobs() {
  const { loading, jobs } = useJobs();

  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("");
  const [sort, setSort] = useState("match");

  const filteredJobs = useMemo(() => {
    let filtered = [...jobs];

    // Search
    if (search.trim()) {
      const query = search.toLowerCase();

      filtered = filtered.filter((job) => {
        return (
          job.title.toLowerCase().includes(query) ||
          job.company.toLowerCase().includes(query) ||
          job.description.toLowerCase().includes(query) ||
          job.skills.some((skill) =>
            skill.toLowerCase().includes(query)
          )
        );
      });
    }

    // Location
    if (location) {
      filtered = filtered.filter((job) =>
        job.location
          .toLowerCase()
          .includes(location.toLowerCase())
      );
    }

    // Sort
    if (sort === "company") {
      filtered.sort((a, b) =>
        a.company.localeCompare(b.company)
      );
    }

    if (sort === "location") {
      filtered.sort((a, b) =>
        a.location.localeCompare(b.location)
      );
    }

    return filtered;
  }, [jobs, search, location, sort]);

  if (loading) {
    return (
      <div className="text-white text-2xl">
        Loading jobs...
      </div>
    );
  }

  return (
    <div className="space-y-8">

      {/* Header */}

      <div>

        <h1 className="text-5xl font-bold">
          Find Your Next Job
        </h1>

        <p className="text-slate-400 mt-3">
          AI-powered job recommendations based on your resume.
        </p>

      </div>

      {/* Search */}

      <SearchBar
        value={search}
        onChange={setSearch}
      />

      {/* Filters */}

      <div className="flex flex-col md:flex-row gap-4 justify-between">

        <FilterBar
          location={location}
          setLocation={setLocation}
        />

        <SortDropdown
          value={sort}
          onChange={setSort}
        />

      </div>

      {/* Count */}

      <div className="text-slate-400">
        {filteredJobs.length} Jobs Found
      </div>

      {/* Empty State */}

      {filteredJobs.length === 0 ? (
        <div className="bg-slate-900 rounded-2xl border border-slate-800 p-12 text-center">

          <h2 className="text-2xl font-bold">
            No jobs found
          </h2>

          <p className="text-slate-400 mt-2">
            Try changing your search or filters.
          </p>

        </div>
      ) : (
        <div className="grid gap-6">

          {filteredJobs.map((job, index) => (
            <JobCard
              key={index}
              job={job}
            />
          ))}

        </div>
      )}

    </div>
  );
}