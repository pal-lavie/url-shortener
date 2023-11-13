import { Box, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { formatDate } from "../utils";
import { AppContext } from "../context/appContext";
import { apiJSONType } from '../apiHandler';
import { GET_URL_DETAILS } from "../api";
import ArrowBackIosRoundedIcon from '@mui/icons-material/ArrowBackIosRounded';
import { useNavigate } from "react-router-dom";

const URLLogs = () => {
    const styles = {
        pageContainer: {
            padding: '2rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '2rem'
        },
        pageHeader: {
            display: 'flex',
            gap: '0.5rem',
            alignItems: 'center'
        }
    }

    const navigate = useNavigate();
    const [urlLogs, setURLLogs] = useState([]);
    const { selectedURLID, setSelectedURLID } = useContext(AppContext)

    const getURLDetails = async () => {
        const res = await apiJSONType.get(`${GET_URL_DETAILS}/${selectedURLID}`)
        if(res.status === 200) {
            setURLLogs(res.data)
        }
    }

    const navigatePreviousPage = () => {
        navigate(-1)
        setSelectedURLID('');
    }

    useEffect(() => {
        if(selectedURLID) {
            getURLDetails();
        }
    }, [selectedURLID]);

    return <Box sx={styles.pageContainer}>
        <Box sx={styles.pageHeader}>
            <Button onClick={navigatePreviousPage}><ArrowBackIosRoundedIcon /></Button>
            <Typography>URL Logs</Typography>
        </Box>
        <TableContainer>
            <Table>
                <TableHead>
                    <TableCell>IP Address</TableCell>
                    <TableCell>User Agent</TableCell>
                    <TableCell>Access Time</TableCell>
                </TableHead>
                <TableBody>
                    {urlLogs.map((log) => (
                        <TableRow>
                            <TableCell>{log?.ip_address}</TableCell>
                            <TableCell>{log?.user_agent}</TableCell>
                            <TableCell>{formatDate(log?.access_time)}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    </Box>
}

export default URLLogs;