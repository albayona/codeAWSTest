import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import HomeIcon from '@mui/icons-material/Home';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import FilterListIcon from '@mui/icons-material/FilterList';
export const items = [
    {
        index: 0,
        href: '/home',
        icon: (
            <HomeIcon fontSize="large"/>
        ),
        label: 'Home'
    },
    {
        index: 1,
        href: '/support',
        icon: (
            <HelpOutlineIcon fontSize="large"/>
        ),
        label: 'Support'
    },
    {
        index: 2,
        href: '/user',
        icon: (
            <AccountBoxIcon fontSize="large"/>
        ),
        label: 'User management'
    },
    {
        index: 3,
        href: '/settings',
        icon: (
            <FilterListIcon fontSize="large"/>
        ),
        label: 'Filter settings'
    },

];
