import { Card, CardContent, Typography } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import dayjs from "dayjs";
import StatusChip from "./StatusChip";

export default function JobTable({ jobs = [], isLoading = false, isError = false }) {
    const columns = [
        { field: "title", headerName: "Title", flex: 1.4, minWidth: 200 },
        { field: "company", headerName: "Company", flex: 1, minWidth: 160 },
        { field: "location", headerName: "Location", flex: 0.8, minWidth: 140 },
        {
            field: "source",
            headerName: "Source",
            width: 110,
            sortable: false,
            renderCell: (p) => <Typography variant="body2">{(p.value || "").toUpperCase()}</Typography>,
        },
        {
            field: "posted_at",
            headerName: "Posted",
            width: 140,
            valueFormatter: (v) => (v.value ? dayjs(v.value).format("DD MMM") : "-"),
        },
        {
            field: "url",
            headerName: "Link",
            width: 90,
            sortable: false,
            renderCell: (p) => (
                <a href={p.value} target="_blank" rel="noreferrer">Open</a>
            ),
        },
    ];

    return (
        <Card>
            <CardContent>
                <DataGrid
                    rows={jobs}
                    columns={columns}
                    getRowId={(row) => row.id}
                    autoHeight
                    loading={isLoading}
                    disableRowSelectionOnClick
                    initialState={{
                        pagination: { paginationModel: { page: 0, pageSize: 10 } },
                        sorting: { sortModel: [{ field: "posted_at", sort: "desc" }] },
                    }}
                    pageSizeOptions={[10, 25, 50]}
                    sx={{
                        "--DataGrid-containerbackground": "transparent",
                        "& .MuiDataGrid-columnHeaders": { bgcolor: "#fafafa" },
                    }}
                />
                {isError && <Typography color="error" sx={{ mt: 1 }}>Failed to load jobs.</Typography>}
            </CardContent>
        </Card>
    );
}