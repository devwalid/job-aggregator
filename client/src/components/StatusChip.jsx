import { Chip } from "@mui/material";

export default function StatusChip({ status }) {
    const color =
        status === "APPLIED" ? "success" :
        status === "SAVED" ? "info" :
        "default";
    return <Chip size="small" color={color} label={status || "NEW"} />;
}