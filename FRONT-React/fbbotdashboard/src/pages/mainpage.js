import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import FullFeaturedCrudGrid from "../components/table";
import {AppBar, Button, TextField, Toolbar} from "@mui/material";
import {API_HOST} from "../hooks/useFetch";
import {useAuth} from "../conntexts/UserContext";

function CustomTabPanel(props) {
    const {children, value, index, ...other} = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && <Box sx={{p: 3}}>{children}</Box>}
        </div>
    );
}

CustomTabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.number.isRequired,
    value: PropTypes.number.isRequired,
};

function a11yProps(index) {
    return {
        id: `simple-tab-${index}`,
        'aria-controls': `simple-tabpanel-${index}`,
    };
}

export default function MainPage() {
    const [value, setValue] = React.useState(0);
    const [scrapeUrl, setScrapeUrl] = React.useState('https://www.facebook.com/marketplace/108610652496213/vehicles?maxPrice=4000&maxMileage=200000&minYear=2007&carType=suv&transmissionType=automatic&exact=false');
    const {token} = useAuth();

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    function scrape() {
        if (scrapeUrl) {
            fetch(`${API_HOST}/scrape/scrape/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({link: scrapeUrl})
            })
                .then(response => {
                    if (!response.ok) {
                        // error coming back from server
                        throw Error('Could not update car');
                    }

                    return response.json();
                })
                .then(() => {
                    console.log('Scrape successful');
                })
                .catch(err => {
                    console.log(err.message);
                })
        }
    }

    return (
        <React.Fragment>
            <AppBar position="static">
                <Toolbar variant="dense">
                    <Button onClick={scrape} variant="contained">Scrape</Button>
                    <TextField
                        id="filled-basic"
                        label="Scrape Url"
                        value={scrapeUrl}
                        onChange={(event) => {
                            setScrapeUrl(event.target.value);
                        }}
                        variant="filled"
                        fullWidth
                    />
                </Toolbar>
            </AppBar>
            <Box sx={{width: '100%'}}>
                <Box sx={{borderBottom: 1, borderColor: 'divider'}}>
                    <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                        <Tab label="New" {...a11yProps(0)} />
                        <Tab label="Archived" {...a11yProps(1)} />
                        <Tab label="Favorites" {...a11yProps(2)} />
                    </Tabs>
                </Box>
                <CustomTabPanel value={value} index={0}>
                    <FullFeaturedCrudGrid url= {`${API_HOST}/list-new/list-new/`} type="New"/>
                </CustomTabPanel>
                <CustomTabPanel value={value} index={1}>
                    <FullFeaturedCrudGrid url={`${API_HOST}/list-old/list-old/`} type="Old"/>
                </CustomTabPanel>
                <CustomTabPanel value={value} index={2}>
                    <FullFeaturedCrudGrid url={`${API_HOST}/list-liked/list-liked/`} type="Favs"/>
                </CustomTabPanel>
            </Box>
        </React.Fragment>
    );
}