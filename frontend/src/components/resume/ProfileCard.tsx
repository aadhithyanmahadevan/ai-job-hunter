import Card from "../common/Card";

import {
    User,
    Briefcase,
    Award,
    CheckCircle2,
} from "lucide-react";

interface Props {
    name: string;
    title: string;
    experience: string;
}

export default function ProfileCard({
    name,
    title,
    experience,
}: Props) {

    return (

        <Card>

            <div className="flex flex-col lg:flex-row justify-between gap-8">

                {/* Left */}

                <div className="flex gap-5">

                    <div
                        className="
                        w-24
                        h-24
                        rounded-full
                        bg-gradient-to-r
                        from-cyan-500
                        to-blue-600
                        flex
                        items-center
                        justify-center
                        shadow-lg
                    "
                    >

                        <User
                            size={46}
                            className="text-white"
                        />

                    </div>

                    <div>

                        <h1 className="text-3xl font-bold">

                            {name}

                        </h1>

                        <div className="flex items-center gap-2 mt-3 text-slate-300">

                            <Briefcase
                                size={18}
                                className="text-cyan-400"
                            />

                            {title}

                        </div>

                        <div className="flex items-center gap-2 mt-2 text-cyan-400">

                            <Award size={18} />

                            {experience} Years Experience

                        </div>

                    </div>

                </div>

                {/* Right */}

                <div className="flex items-center">

                    <div
                        className="
                        px-5
                        py-3
                        rounded-xl
                        bg-green-500/20
                        border
                        border-green-500/40
                        flex
                        items-center
                        gap-3
                    "
                    >

                        <CheckCircle2
                            className="text-green-400"
                            size={22}
                        />

                        <div>

                            <p className="text-sm text-slate-400">

                                AI Status

                            </p>

                            <h3 className="font-semibold text-green-400">

                                Verified

                            </h3>

                        </div>

                    </div>

                </div>

            </div>

        </Card>

    );

}