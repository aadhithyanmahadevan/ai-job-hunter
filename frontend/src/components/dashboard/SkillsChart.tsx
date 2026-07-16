import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer
} from "recharts";

const data = [
    { name: "Java", value: 35 },
    { name: "Selenium", value: 25 },
    { name: "AWS", value: 20 },
    { name: "Docker", value: 20 },
];

const COLORS = [
    "#06b6d4",
    "#3b82f6",
    "#6366f1",
    "#8b5cf6",
];

export default function SkillsChart() {
    return (
        <div className="h-80">

            <ResponsiveContainer width="100%" height="100%">

                <PieChart>

                    <Pie
                        data={data}
                        dataKey="value"
                        outerRadius={100}
                        label
                    >

                        {data.map((_, index) => (

                            <Cell
                                key={index}
                                fill={COLORS[index % COLORS.length]}
                            />

                        ))}

                    </Pie>

                    <Tooltip />

                </PieChart>

            </ResponsiveContainer>

        </div>
    );
}