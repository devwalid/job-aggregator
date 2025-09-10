import { alpha, Box, IconButton, InputBase } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import CloseIcon from "@mui/icons-material/Close";
import { useEffect, useMemo, useState } from "react";

export default function SearchBar({ value, onChange, delay = 300 }) {
    const [local, setLocal] = useState(value || "");

    useEffect(() => setLocal(value || ""), [value]);

    const debounced = useMemo(() => {
        let t;
        return (v) => {
            clearTimeout(t);
            t = setTimeout(() => onChange?.(v), delay);
        };
    }, [onChange, delay]);

    const handleChange = (e) => {
        const v = e.target.value;
        setLocal(v);
        debounced(v);
    };

    return (
        <Box
            sx={{
                ml: "auto",
                bgcolor: (t) => alpha(t.palette.primary.main, 0.06),
                border: (t) => `1px solid ${alpha(t.palette.primary.main, 0.15)}`,
                px: 1.5, py: 0.5, borderRadius: 2, display: "flex", alignItems: "center", gap: 1, width: 360
            }}
        >
            <SearchIcon fontSize="small" color="primary" />
            <InputBase
                placeholder="Search title, company, location..."
                sx={{ width: "100%" }}
                value={local}
                onChange={handleChange}
            />
            {!!local && (
                <IconButton size="small" onClick={() => { setLocal(""); onChange?.(""); }}>
                    <CloseIcon fontSize="small" />
                </IconButton>
            )}
        </Box>
    );
}