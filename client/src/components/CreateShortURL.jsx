import { Box, Dialog, Typography, Button, TextField, DialogActions, DialogTitle, DialogContent } from "@mui/material"
import React, { useState } from "react";
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';
import { colorPalette } from "../colors";
import { DateTimePicker } from "@mui/x-date-pickers";
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import dayjs, { Dayjs } from 'dayjs';


const CreateShortURL = ({open, onClose, onSubmit}) => {
    const [urlDetails, setURLDetails] = useState({
        url: '',
        expiryDate: null,
        usageLimit: null,
    })
    const styles = {
        dialogHeader: {
            display:'flex',
            justifyContent: 'space-between',
            marginBottom: '0.5rem',
            alignItems: 'center'
        },
        dialogContent: {
            display: 'flex',
            flexDirection: 'column',
            paddingTop: '1rem',
            gap: '1rem',
        },
        dialogActions: {
            paddingBottom: '2rem',
            paddingRight: '1.5rem',
            display: 'flex'
        },
        submitButton: {
            textTransform: 'none'
        },
        closeIcon: {
            color: colorPalette.primary,
            cursor: 'pointer',
        }
    }

    const clearFields = () => {
        setURLDetails({
            url: '',
            expiryDate: null,
            usageLimit: null,
        })
    }

    const closeHandler = () => {
        onClose();
        clearFields();
    }

    return <Dialog open={open} onClose={closeHandler} fullWidth={true}>
        <DialogTitle sx={styles.dialogHeader}>
            <Typography>Create Short URL</Typography>
            <CloseRoundedIcon onClick={closeHandler} sx={styles.closeIcon} />
        </DialogTitle>
        <DialogContent sx={styles.dialogContent}>
            <TextField id="outlined-basic" label="URL" placeholder="URL" variant="outlined" value={urlDetails.url} onChange={(event) => setURLDetails({...urlDetails, url: event.target.value})} />
            <TextField id="outlined-basic" label="API Usage Limit" type="Number" placeholder="API Usage Limit" variant="outlined" value={urlDetails.usageLimit} onChange={(event) => setURLDetails({...urlDetails, usageLimit: Number(event.target.value)})} />
            <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DateTimePicker label="Expiry date" disablePast={true} value={urlDetails?.expiryDate} onChange={(event) => setURLDetails({...urlDetails, expiryDate: event?.$d})} />
            </LocalizationProvider>
        </DialogContent>
        <DialogActions sx={styles.dialogActions}>
        <Button variant="contained" onClick={() => {
            onSubmit(urlDetails);
            clearFields();
        }} sx={styles.submitButton}>Create URL</Button>
        <Button variant="outlined" onClick={closeHandler} sx={styles.submitButton}>Cancel</Button>
        </DialogActions>
    </Dialog>
}

export default CreateShortURL;