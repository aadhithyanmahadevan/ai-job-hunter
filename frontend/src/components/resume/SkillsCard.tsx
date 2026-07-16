import Card from "../common/Card";
import { Code2 } from "lucide-react";

interface Props {
    skills: string[];
}

export default function SkillsCard({
    skills,
}: Props) {

    return (

        <Card title="Technical Skills">

            <div className="flex flex-wrap gap-3">

                {skills.map((skill) => (

                    <div
                        key={skill}
                        className="
                            px-4
                            py-2
                            rounded-full
                            bg-cyan-500/15
                            border
                            border-cyan-500/30
                            text-cyan-300
                            flex
                            items-center
                            gap-2
                            hover:bg-cyan-500/25
                            transition
                            duration-300
                        "
                    >

                        <Code2 size={16} />

                        {skill}

                    </div>

                ))}

            </div>

        </Card>

    );

}