import { Container, Stack, Typography, Snackbar, Alert } from "@mui/material";
import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { fetchJobs, getLastRefreach, collectNow } from "../api/jobs";
import FiltersBar from "../components/FilterBar";
import JobTable from "../components/JobTable";
import LastRefresh from "../components/LastRefreash";
import JobDetailsDialog from "../components/JobDetailsDialog";

export default function JobsPage({ q }) {
    const [source, setSource] = useState("");
    const [status, setStatus] = useState("");
    const [selected, setSelected] = useState(null);
    const [open, setOpen] = useState(false);
    const qc = useQueryClient();

    const jobsQuery = useQuery({
        queryKey: ["jobs", { q, source, status }],
        queryFn: () => fetchJobs({ q, source, status }),
        refetchOnWindowFocus: false,
    });

    const lastQuery = useQuery({
        queryKey: ["last_refresh"],
        queryFn: getLastRefreach,
        refetchInterval: 60_000,
    });

    const [toast, setToast] = useState(null);

    const collectMutation = useMutation({
        mutationFn: collectNow,
        onSuccess: (res) => {
            setToast(`Collected ${res.inserted_or_updated} items`);
            qc.invalidateQueries({ queryKey: ["jobs"] });
            qc.invalidateQueries({ queryKey: ["last_refresh"]});
        },
        onError: (err) => setToast(`Collect failed: ${err?.response?.data?.detail || err.message}`),
    });

    const { data = [], isLoading, isError } = useQuery({
        queryKey: ["jobs", { q, source,status }],
        queryFn: () => fetchJobs({ q, source, status }),
        refetchOnWindowFocus: false,
    });

    const handleRowClick = (row) => {
        setSelected(row);
        setOpen(true);
    };

    return (
            <Container maxWidth="lg" sx={{ py: 3 }}>
                <Stack gap={2}>
                    <Typography variant="h6">Jobs</Typography>

                    <LastRefresh
                        last={lastQuery.data?.last_refresh}
                        total={lastQuery.data?.total}
                        loading={collectMutation.isPending}
                        onCollect={() => collectMutation.mutate()}
                    />

                    <FiltersBar
                        source={source}
                        status={status}
                        onSource={setSource}
                        onStatus={setStatus}
                    />
                    <JobTable
                        jobs={data}
                        isLoading={isLoading}
                        isError={isError}
                        onRowClick={handleRowClick}
                    />

                    <JobDetailsDialog open={open} onClose={() => setOpen(false)} job={selected} />

                    <Snackbar
                        open={!!toast}
                        autoHideDuration={3000}
                        onClose={() => setToast(null)}
                        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
                    >
                        <Alert severity="info" variant="filled" onClose={() => setToast(null)}>
                            {toast}
                        </Alert>
                    </Snackbar>
                </Stack>
            </Container>
    );
}