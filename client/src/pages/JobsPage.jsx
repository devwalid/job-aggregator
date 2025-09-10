import { Container, Stack, Typography } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { fetchJobs } from "../api/jobs";
import FiltersBar from "../components/FilterBar";
import JobTable from "../components/JobTable";

export default function JobsPage({ q }) {
    const [source, setSource] = useState("");
    const [status, setStatus] = useState("");

    const { data = [], isLoading, isError } = useQuery({
        queryKey: ["jobs", { q, source,status }],
        queryFn: () => fetchJobs({ q, source, status }),
        refetchOnWindowFocus: false,
    });

    return (
        <Container maxWidth="lg" sx={{ py: 3 }}>
            <Stack gap={2}>
                <Typography variant="h6">Jobs</Typography>
                <FiltersBar
                    source={source}
                    status={status}
                    onSource={setSource}
                    onStatus={setStatus}
                />
                <JobTable jobs={data} isLoading={isLoading} isError={isError} />
            </Stack>
        </Container>
    );
}