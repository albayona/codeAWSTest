import { Link as RouterLink } from 'react-router-dom';
import { Box, Button, Container, Typography } from '@mui/material';

const NotAuthorized = () => (
    <>

        <Box
            sx={{
                backgroundColor: 'background.paper',
                flexGrow: 1
            }}
        >
            <Container
                maxWidth="md"
                sx={{
                    px: 5,
                    py: 14,
                    alignItems: 'center',
                    display: 'flex',
                    flexDirection: 'column'
                }}
            >
                <Box
                    sx={{
                        '& img': {
                            maxWidth: '100%'
                        }
                    }}
                >
                </Box>
                <Typography
                    align="center"
                    sx={{ my: 2 }}
                    variant="h3"
                >
                    Not Authorized
                </Typography>
                <Typography
                    align="center"
                    color="text.secondary"
                    variant="body2"
                >
                    Contact the administrator to request access to the system.
                </Typography>
                <Button
                    to="/"
                    component={RouterLink}
                    sx={{ mt: 2 }}
                >
                    Home
                </Button>
            </Container>
        </Box>
    </>
);

export default NotAuthorized;
