import { useState } from "react";
import axios from "axios";
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

type DataPoint = { date: string; temperature: number };

function App() {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [data, setData] = useState<DataPoint[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const fetchSpaceVariations = async () => {
        if (!startDate || !endDate) return;
        setLoading(true);
        setError("");

        try {
            const response = await axios.get(
                `http://localhost:8000/get_space_objects_variation/`,
                {
                    params: {
                        begin: startDate,
                        end: endDate,
                    },
                }
            );

            const time: string[] = response.data.days;
            const variations: number[] = response.data.variations;

            const result = time.map((t, i) => ({ date: t, variation: variations[i] }));
            setData(result);
        } catch (err: any) {
            setError(`Failed to fetch data. ${err}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "2rem", fontFamily: "Arial", width: '100%', height: 'auto' }}>
            <h2>Variation of objects in space</h2>
            <div style={{ marginBottom: "1rem" }}>
                <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
                <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
                <button onClick={fetchSpaceVariations} disabled={loading || !startDate || !endDate}>
                    {loading ? "Loading..." : "Fetch data"}
                </button>
            </div>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {data.length > 0 && (
                <ResponsiveContainer width="95%" height={400}>
                    <LineChart data={data}>
                        <CartesianGrid stroke="#ccc" />
                        <XAxis dataKey="date" />
                        <YAxis label={{ value: "Launches - Reentries", angle: -90, position: "center" }} />
                        <Tooltip />
                        <Line type="monotone" dataKey="variation" stroke="#ff7300" />
                    </LineChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}

export default App;

