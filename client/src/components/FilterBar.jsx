import { Box, FormControl, InputLabel, MenuItem, Select, Stack } from "@mui/material";

const SOURCES = ["", "hn", "indeed"];
const STATUSES = ["", "NEW", "SAVED", "APPLIED"];

export default function FiltersBar({ source, status, onSource, onStatus }) {
    return (
        <Stack direction="row" spacing={2} sx={{ mb: 1}}>
            <FormControl size="small" sx={{ minWidth: 160 }}>
                <InputLabel>Source</InputLabel>
                <Select label="Source" value={source} onChange={(e) => onSource?.(e.target.value)}>
                    {SOURCES.map((s) => <MenuItem key={s || "all"} value={s}>{s ? s.toUpperCase() : "All"}</MenuItem>)}
                </Select>
            </FormControl>
            <FormControl size="small" sx={{ minWidth: 160 }}>
                <InputLabel>Status</InputLabel>
                <Select label="Status" value={status} onChange={(e) => onStatus?.(e.target.value)}>
                    {STATUSES.map((s) => <MenuItem key={s || "all"} value={s}>{s || "All"}</MenuItem>)}
                </Select>
            </FormControl>
            <Box sx={{ flex: 1 }} />
        </Stack>
    );
}