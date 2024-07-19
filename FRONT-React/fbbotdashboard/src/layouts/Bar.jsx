import {useAuth} from "../conntexts/UserContext";
import AdminNav from "./AdminBar";
import LandingBar from "./LandingBar";

const Bar = () => {

    const {user}  = useAuth();
    console.log(user);
    return user ? <AdminNav/> : <LandingBar/>;
};

export default Bar;