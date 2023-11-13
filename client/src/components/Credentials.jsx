import { Box, Button, TextField } from "@mui/material"
import React, { useState } from "react";
import { colorPalette } from "../colors";

const Credentials = ({onSubmit, buttonText = "", doesEmailExist = false}) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('')

    const styles = {
        parent: {
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
        },
        submitButton: {
            textTransform: 'none'
        }   
    }

    const clearFields = () => {
        setUsername('');
        setPassword('');
        setEmail('');
    }

    const onFormSubmit = async () => {
        doesEmailExist ?  onSubmit({username, password, email}) : onSubmit({username, password});
        clearFields();
    }

    return <Box sx={styles.parent}>
       <TextField id="outlined-basic" label="Username" variant="outlined" value={username} onChange={(event) => setUsername(event.target.value)} />
       <TextField id="outlined-basic" label="Password" variant="outlined" value={password} onChange={(event) => setPassword(event.target.value)} type="password" />
       {doesEmailExist && <TextField id="outlined-basic" label="Email" variant="outlined" value={email} onChange={(event) => setEmail(event.target.value)} />}
       <Button variant="contained" onClick={onFormSubmit} sx={styles.submitButton}>{buttonText}</Button>
    </Box>
}

export default Credentials;