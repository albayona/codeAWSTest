import { styled } from '@mui/material/styles';
import PropTypes from 'prop-types';
import { Footer } from './Footer';
import { SideNav } from './SideNav';
import {Outlet} from "react-router-dom";


const SIDE_NAV_WIDTH = 250;
const TOP_NAV_HEIGHT = 64;

const LayoutRoot = styled('div')(({ theme }) => ({
  backgroundColor: theme.palette.background.default,
  display: 'flex',
  flex: '1 1 auto',
  maxWidth: '100%',
  marginLeft: SIDE_NAV_WIDTH,
}));

const LayoutContainer = styled('div')({
  display: 'flex',
  flex: '1 1 auto',
  flexDirection: 'column',
  width: '100%'
});



const Layout = (props) => {
  const { children } = props;

  return (
    <>
      <SideNav width={SIDE_NAV_WIDTH}  height={TOP_NAV_HEIGHT}/>
      <LayoutRoot>
        <LayoutContainer sx={{marginTop: 8}}>
          {children}
          <Footer />
        </LayoutContainer>
      </LayoutRoot>
    </>
  );
};

Layout.propTypes = {
  children: PropTypes.node
};

const DashboardLayout = () => {

  return (
    <Layout>
      <Outlet />
    </Layout>
  );
};

export default DashboardLayout;