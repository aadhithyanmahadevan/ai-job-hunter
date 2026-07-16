import Card from "../common/Card";
import { GraduationCap } from "lucide-react";

interface Props {
    education: string[];
}

export default function EducationCard({
    education,
}: Props) {

    return (

        <Card title="Education">

            <div className="space-y-4">

                {education.map((item, index) => (

                    <div
                        key={index}
                        className="
                            flex
                            gap-4
                            items-start
                            border-l-2
                            border-cyan-500
                            pl-4
                        "
                    >

                        <GraduationCap
                            className="text-cyan-400 mt-1"
                            size={20}
                        />

                        <div>

                            <p className="font-medium">

                                {item}

                            </p>

                        </div>

                    </div>

                ))}

            </div>

        </Card>

    );

}