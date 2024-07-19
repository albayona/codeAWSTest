import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import {useAuth} from "../conntexts/UserContext";
import {Alert, Paper} from "@mui/material";
import {useNavigate} from "react-router-dom";
import {useEffect} from "react";
import {API_HOST} from "../hooks/useFetch";


function Copyright(props) {
    return (<Typography variant="body2" color="text.secondary" align="center" {...props}>
        {'Copyright © '}
        <Link color="inherit">
            Andy
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
    </Typography>);
}

export default function LogIn() {

    const [input, setInput] = React.useState({
        username: "", password: "", role: "",
    });

    const [usernameError, setUsernameError] = React.useState(false);
    const [passError, setPassError] = React.useState(false);
    const [authError, setAuthError] = React.useState("");
    const [loginEvent, setLoginEvent] = React.useState(false);

    const {loginAction} = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (loginEvent) {
            fetch(`${API_HOST}/token/token/`, {
                method: 'POST', headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify({
                    username: input.username, password: input.password
                })
            })
                .then(response => {
                    if (!response.ok) {
                        // error coming back from server
                        throw Error('Invalid credentials');
                    }
                    return response.json();
                })
                .then(data => {

                    console.log(data);

                    loginAction({
                        token: data.access,
                        user: {
                            email: input.username, role: "admin",
                        }
                    });

                    setPassError(false);
                    setUsernameError(false);
                    setAuthError("");
                    setLoginEvent(false);
                    navigate("/home");

                })
                .catch(err => {
                    setAuthError(err.message);
                    setLoginEvent(false);
                })
        }

    }, [loginEvent])

    const handleSubmit = (event) => {

        event.preventDefault();
        let b = input.password === "";
        setPassError(b);
        let b1 = input.username === "";
        setUsernameError(b1);

        if (!(b || b1)) {
            setLoginEvent(true);
        }
    };

    const handleChange = (e) => {
        setInput({
            ...input, [e.target.name]: e.target.value,
        });
    }

    return (<Grid container component="main" sx={{height: '100vh'}}>

        {/*<CssBaseline />*/}
        <Grid
            item
            xs={false}
            sm={4}
            md={7}
            sx={{


                backgroundImage: 'url(bg.jpg)',
                backgroundRepeat: 'no-repeat',
                backgroundColor: (t) => t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
                backgroundSize: 'cover',
                backgroundPosition: 'center',
            }}
        />
        <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square={false}>
            <Box

                sx={{
                    my: 8, mx: 4, display: 'flex', flexDirection: 'column', alignItems: 'center',
                }}
            >
                <Avatar sx={{m: 1, bgcolor: 'secondary.main'}}>
                    <LockOutlinedIcon/>
                </Avatar>
                <Typography component="h1" variant="h5">
                    Log in
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate sx={{mt: 1}}>
                    <TextField
                        error={usernameError}
                        helperText="Username is required"
                        onChange={e => handleChange(e)}
                        margin="normal"
                        required={true}
                        fullWidth
                        id="username"
                        label="username"
                        name="username"
                        autoComplete="username"
                        autoFocus
                    />
                    <TextField
                        error={passError}
                        helperText="Password is required"
                        err
                        onChange={e => handleChange(e)}
                        margin="normal"
                        required={true}
                        fullWidth
                        name="password"
                        label="password"
                        type="password"
                        id="password"
                        autoComplete="current-password"
                    />
                    <FormControlLabel
                        control={<Checkbox value="remember" color="primary"/>}
                        label="Remember me"
                    />

                    {authError && <Alert severity="error">{authError}</Alert>}
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{mt: 3, mb: 2}}
                    >
                        Log in
                    </Button>
                    <Grid container>
                        <Grid item xs>
                            <Link href="src/pages/LogIn#" variant="body2">
                                Recover password
                            </Link>
                        </Grid>
                        <Grid item>
                            <Link href="src/pages/LogIn#" variant="body2">
                                {"Sign up"}
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
                <Copyright sx={{mt: 5}}/>
            </Box>
        </Grid>
    </Grid>);
}

