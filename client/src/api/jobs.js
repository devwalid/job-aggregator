import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export async function fetchJobs({ q = "", source = "", status = "", from = "", to ="" }) {
    const res = await axios.get(`${API_URL}/jobs`, {
        params: {
            q,
            source: source || undefined,
            status: status || undefined,
            from_date: from || undefined,
            to_date: to || undefined,
            limit: 200,
        },
    });
    return res.data;
}