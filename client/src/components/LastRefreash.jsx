import { Chip, Stack, Button, Tooltip } from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
dayjs.extend(relativeTime);

export default function LastRefresh({ last, total, onCollect, loading }) {
    const label = last ? `Last refresh: ${dayjs(last).fromNow()}` : "Last refresh: —";
    return (
        <Stack direction="row" spacing={2} alignItems="center">
            <Tooltip title={last ? dayjs(last).format("YYYY-MM-DD HH:mm:ss") : ""} arrow>
                <Chip label={label} variant="outlined" />
            </Tooltip>
            <Chip label={`Total: ${total ?? 0}`} variant="outlined" />
            <Button
                variant="contained"
                size="small"
                startIcon={<RefreshIcon />}
                onClick={onCollect}
                disabled={loading}
            >
                {loading ? "Refreshing..." : "Collect now"}
            </Button>
        </Stack>
    );
}