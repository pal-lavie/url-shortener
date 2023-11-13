import { Box, Button, Typography } from "@mui/material";
import Credentials from "./Credentials";
import { colorPalette } from "../colors";
import { useNavigate } from 'react-router-dom';
import { apiFormType } from "../apiHandler";
import { LOGIN } from "../api";
import { useAppContext } from "../context/appContext";
import { DASHBOARD_ROUTE } from "../routes";


const Login = () => {
    const styles = {
        loginPage: {
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

    const { setAccessToken } = useAppContext();
    const navigate = useNavigate();

    const loginUser = async (userDetails) => {
        const res = await apiFormType.post(LOGIN, userDetails);
        if(res.status === 200) {
            const accessToken = res.data.access_token;
            localStorage.setItem('access_token', accessToken)
            setAccessToken(accessToken);
            navigate(DASHBOARD_ROUTE)
        }
        console.log({res})
    };

    const redirectToSignup = () => {
        navigate('/register')
    }

    return <Box sx={styles.loginPage}>
        <Credentials buttonText="Login" onSubmit={loginUser} />
        <Box sx={styles.subText}>
            <Button sx={styles.redirectButton} onClick={redirectToSignup}>Create an account</Button>
        </Box>
    </Box>
}

export default Login;