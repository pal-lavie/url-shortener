import { Box, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material"
import { useEffect, useState } from "react";
import CreateShortURL from "./CreateShortURL";
import { useAppContext } from "../context/appContext";
import { useNavigate } from "react-router-dom";
import { LOGIN_ROUTE, URL_LOGS } from "../routes";
import { apiJSONType } from '../apiHandler';
import { CREATE_SHORT_URL, GET_ALL_URLS } from "../api";
import ChevronRightRoundedIcon from '@mui/icons-material/ChevronRightRounded';
import FileCopyOutlinedIcon from '@mui/icons-material/FileCopyOutlined';

import dayjs from "dayjs";
import { formatDate } from "../utils";

const Dashboard = () => {
    const styles = {
        pageContainer: {
            width: '100%',
            padding: '1.5rem',
            display: 'flex',
            justifyContent: 'space-between'
        },
        pageTable: {
            display: 'flex',
            flexDirection: 'column',
            gap: '2rem'
        },
        clickableRow: {
            cursor: 'pointer'
        }
    }
    const [openCreateURLDialog, setOpenCreateURLDialog] = useState(false);
    const { setAccessToken, setSelectedURLID } = useAppContext();
    const [urls, setURLs] = useState([]);
    const navigate = useNavigate();
    const [isCopied, setIsCopied] = useState(false);

    const onCreateShortURL = async (urlDetails) => {
        const payload = {
            original_url: urlDetails.url,
            expiry: dayjs(urlDetails.expiryDate).format('YYYY-MM-DDTHH:mm:ss[Z]'),
            remaining_uses: urlDetails.usageLimit
        }
        console.log({payload})
        const res = await apiJSONType.post(CREATE_SHORT_URL, payload)
        if(res.status === 200) {
            getAllURLS();
        }
        closeDialog();
    }

    const closeDialog = () => {
        setOpenCreateURLDialog(false);
    }

    const getAllURLS = async () => {
        const res = await apiJSONType.get(GET_ALL_URLS);
        if(res.status === 200 && res.data) {
            setURLs(res.data)
        }
        console.log({res})
    }

    const showURLDetails = (urlID) => {
        setSelectedURLID(urlID);
        navigate(URL_LOGS)
    }

    const copyToClipboard = async (event, text) => {
        event.stopPropagation();
        try {
          await navigator.clipboard.writeText(text);
          setIsCopied(true);
        } catch (err) {
          console.error('Unable to copy to clipboard', err);
        }
    };

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        console.log({token})
        getAllURLS();
        
    }, [])

    return <Box sx={styles.pageContainer}>
       <Box sx={styles.pageTable}>
        <Typography>List of Generated URLs</Typography>
        <TableContainer>
            <Table>
                <TableHead>
                    <TableCell>Original URL</TableCell>
                    <TableCell>Short URL</TableCell>
                    <TableCell>URL Usage Limit</TableCell>
                    <TableCell>Remaining Uses</TableCell>
                    <TableCell>Expiry Date</TableCell>
                    <TableCell>Created At</TableCell>
                    <TableCell>Status</TableCell>
                    {/* <TableCell>Views</TableCell> */}
                    <TableCell></TableCell>
                </TableHead>
                <TableBody>
                    {urls.map((url) => (
                    <TableRow sx={styles.clickableRow} onClick={() => showURLDetails(url?.id)}>
                        <TableCell>{url?.original_url}</TableCell>
                        <TableCell><a>{url?.short_code}</a>
                            <Button onClick={(event) => copyToClipboard(event, url?.short_code)}>
                                <FileCopyOutlinedIcon />
                            </Button>
                        </TableCell>
                        <TableCell>{url?.url_use_limit ? 'yes' : 'no'}</TableCell>
                        <TableCell>{url?.remaining_uses >= 0 ? url?.remaining_uses : '-'}</TableCell>
                        <TableCell>{url?.expiry ? formatDate(url?.expiry) : '-'}</TableCell>
                        <TableCell>{url?.created_at ? formatDate(url?.created_at) : '-'}</TableCell>
                        <TableCell>{url?.is_active ? 'Active' : 'Inactive'}</TableCell>
                        {/* <TableCell>{url?.views}</TableCell> */}
                        <TableCell><Button><ChevronRightRoundedIcon /></Button></TableCell>
                    </TableRow>))}
                </TableBody>
            </Table>
        </TableContainer>
       </Box>
        <Box> 
            <Button variant="contained" onClick={() => setOpenCreateURLDialog(true)}>Create Short URL</Button>
        </Box>
        <CreateShortURL 
        open={openCreateURLDialog}
        onClose={closeDialog}
        onSubmit={onCreateShortURL}
         />
    </Box>
}

export default Dashboard;