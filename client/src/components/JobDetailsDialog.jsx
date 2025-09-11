import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Chip, Stack, Typography, Link } from "@mui/material";
import dayjs from "dayjs";

export default function JobDetailsDialog({ open, onClose, job }) {
    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle>Job Details</DialogTitle>
            <DialogContent dividers>
                {!job ? (
                    <Typography variant="body2" color="text.secondary">No job selected</Typography>
                ) : (
                    <Stack spacing={1.2}>
                        <Stack direction="row" spacing={1}>
                            <Chip label={(job.source || "").toUpperCase()} size="small"/>
                            <Chip label={job.stattus || "NEW"} size="small" variant="outlined" />
                        </Stack>
                        <Typography variant="h6" fontWeight={700}>{job.title}</Typography>
                        {job.company && <Typography>{job.company}</Typography>}
                        {job.location && <Typography color="text.secondary">{job.location}</Typography>}
                        {job.posted_at && (
                            <Typography color="text.secondary">
                                posted: {dayjs(job.posted_at).format("DD MM YYYY HH:mm")}
                            </Typography>
                        )}
                        {job.url && (
                            <Link href={job.url} target="_blank" rel="noreferrer" underline="hover">
                                Open listing
                            </Link>
                        )}
                    </Stack>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
}