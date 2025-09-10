import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
    palette: {
        mode: "light",
        primary: { main: "#2563eb"},
        secondary: { main: "#7c3aed" },
        background: { default: "#f7f8fa", paper: "#ffffff" },
        success: { main: "#16a34a" },
        warning: { main: "#d97706" },
        error: { main: "#dc2626" },
        info: { main: "#0284c7" },
    },
    shape: { borderRadius: 14 },
    typography: {
        fontFamily: [
            "Inter",
            "ui-sans-serif",
            "system-ui",
            "Segoe UI",
            "Roboto",
            "Helvetica Neue",
            "Arial",
        ].join(","),
        h6: { fontWeight: 600},
        button: { textTransform: "none", fontWeight: 600},
    },
});