import { AppBar, Toolbar, Typography, Box } from "@mui/material";
import { Routes, Route } from "react-router-dom";
import { useState } from "react";
import SearchBar from "./components/SearchBar";
import JobsPage from "./pages/JobsPage";

export default function App() {
  const [q, setQ] = useState("");

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "Background.default" }}>
      <AppBar position="sticky" color="inherit" elevation={0} sx={{ borderBottom: "1px solid #e5e7eb" }}>
        <Toolbar sx={{ gap:2 }}>
          <Typography variant="h6" color="primary">Job Aggregator</Typography>
          <SearchBar value={q} onChange={setQ} />
        </Toolbar>
      </AppBar>

      <Routes>
        <Route path="/" element={<JobsPage q={q} /> } />
      </Routes>
    </Box>
  );
}