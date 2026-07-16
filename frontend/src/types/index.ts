export interface Resume {
    name: string;
    title: string;
    skills: string[];
    strengths: string[];
    missing_skills: string[];
}

export interface Job {
    title: string;
    company: string;
    location: string;
    salary: string;
    skills: string[];
    url: string;
}