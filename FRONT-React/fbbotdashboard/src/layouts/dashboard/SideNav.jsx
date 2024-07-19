import {Link as RouterLink, matchPath, useLocation} from 'react-router-dom';
import {
    Drawer,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Stack,
    ThemeProvider,
    useTheme
} from '@mui/material';
import {items} from './config';
import React from 'react';
import {createTheme} from "@mui/material/styles";


export const SideNav = ({width, height}) => {
    const location = useLocation();
    const [selectedIndex, setSelectedIndex] = React.useState(1);

    const handleListItemClick = (event, index) => {
        setSelectedIndex(index);
    };

    const globalTheme = useTheme();
    const sideNavTheme = createTheme(globalTheme,{
        components: {
            // Name of the component
            MuiListItemButton: {
                styleOverrides: {
                    // Name of the slot
                    // Some CSS
                    root: ({ownerState}) => ({
                        ...(ownerState.selected === true && {
                            backgroundColor: globalTheme.palette.primary.main + '!important'
                        }),

                    }),

                },
            },
            MuiListItemIcon: {
                styleOverrides: {
                    root: ({ownerState}) => ({
                        color: (ownerState["aria-selected"] === true ? globalTheme.palette.text.contrastText : globalTheme.palette.text.secondary) + '!important',
                        minWidth: 'auto',
                    }),


                }
            },
            MuiListItemText: {
                styleOverrides: {
                    primary: ({ownerState}) => ({
                        color: (ownerState["aria-selected"] === true ? globalTheme.palette.text.contrastText : globalTheme.palette.text.secondary) + '!important',
                        minWidth: 'auto',
                    }),


                }
            },

        },
    });

    return (

        <Drawer
            open
            variant="permanent"
            PaperProps={{
                sx: {
                    backgroundColor: 'background.default',
                    display: 'flex',
                    flexDirection: 'column',
                    height: `calc(100% - ${height}px)`,
                    p: 0,
                    top: height,
                    width: width,
                    zIndex: (theme) => theme.zIndex.appBar - 100
                }
            }}
        >
            <List sx={{width: '100%'}}>
                {items.map((item) => {
                    const active = matchPath({path: item.href, end: true}, location.pathname);

                    return (
                        <ListItem
                            disablePadding
                            component={RouterLink}
                            key={item.href}
                            to={item.href}
                        >
                            <ThemeProvider theme={sideNavTheme}>
                                <ListItemButton
                                    selected={
                                        selectedIndex === item.index
                                    }
                                    onClick={(event) => handleListItemClick(event, item.index)}
                                >

                                    <Stack spacing={2} direction="row" alignItems="center">
                                        <ListItemIcon
                                            aria-selected={selectedIndex === item.index}
                                        >
                                            {item.icon}
                                        </ListItemIcon>

                                        <ListItemText
                                            aria-selected={selectedIndex === item.index}
                                            disableTypography={false}
                                            primary={item.label}
                                            primaryTypographyProps={{
                                                variant: 'h7',
                                            }}
                                        />

                                        <ListItemText/>
                                    </Stack>
                                </ListItemButton>
                            </ThemeProvider>


                        </ListItem>
                    )
                        ;
                })}
            </List>
        </Drawer>
    )
        ;
};
