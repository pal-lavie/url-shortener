import { Box, Button, Typography } from "@mui/material";
import Credentials from "./Credentials";
import { useNavigate } from 'react-router-dom';
import { colorPalette } from "../colors";
import { apiJSONType } from "../apiHandler";
import {  REGISTER } from "../api";
import { LOGIN_ROUTE } from "../routes";

const Signup = () => {
    const styles = {
        signUpPage: {
            backgroundColor: colorPalette.secondary,
            width: '100%',
            height: '100vh',
            display:'flex',
            justifyContent: 'center',
            alignItems: 'center',
            flexDirection: 'column',
            gap: '2rem'
        },
        subText: {
            display: 'flex',
            alignItems: 'center'
        },
        redirectButton: {
            textTransform: 'none',
            color: colorPalette.primary,
        }
    }

    const navigate = useNavigate();

    const createUser = async (userDetails) => {
        const res = await apiJSONType.post(REGISTER, userDetails)
        if(res.status === 201) {
            navigate(LOGIN_ROUTE)
        } else {
            console.log("Error", res)
        }
    };

    const redirectToLogin = () => {
        navigate(LOGIN_ROUTE)
    }

    return <Box sx={styles.signUpPage}>
        <Credentials buttonText="Register" onSubmit={createUser} doesEmailExist={true} />
        <Box sx={styles.subText}>
            <Typography>Already a user?</Typography>
            <Button sx={styles.redirectButton} onClick={redirectToLogin}>Login</Button>
        </Box>
    </Box>
}

export default Signup;