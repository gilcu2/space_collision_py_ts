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

    const fetchTemperature = async () => {
        if (!startDate || !endDate) return;
        setLoading(true);
        setError("");

        try {
            const response = await axios.get(
                `https://archive-api.open-meteo.com/v1/era5`,
                {
                    params: {
                        latitude: 52.52,
                        longitude: 13.41,
                        start_date: startDate,
                        end_date: endDate,
                        daily: "temperature_2m_max",
                        timezone: "Europe/Berlin",
                    },
                }
            );

            const time: string[] = response.data.daily.time;
            const temps: number[] = response.data.daily.temperature_2m_max;

            const result = time.map((t, i) => ({ date: t, temperature: temps[i] }));
            setData(result);
        } catch (err: any) {
            setError("Failed to fetch data.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "2rem", fontFamily: "Arial" }}>
            <h2>🌤️ Temperature Chart</h2>
            <div style={{ marginBottom: "1rem" }}>
                <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
                <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} />
                <button onClick={fetchTemperature} disabled={loading || !startDate || !endDate}>
                    {loading ? "Loading..." : "Fetch"}
                </button>
            </div>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {data.length > 0 && (
                <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={data}>
                        <CartesianGrid stroke="#ccc" />
                        <XAxis dataKey="date" />
                        <YAxis label={{ value: "°C", angle: -90, position: "insideLeft" }} />
                        <Tooltip />
                        <Line type="monotone" dataKey="temperature" stroke="#ff7300" />
                    </LineChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}

export default App;

