import './App.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import {ThemeProvider} from "@mui/material";
import {CustomThemeOptions} from "./styles/CustomTheme";
import MainPage from "./pages/mainpage";
import UserProvider from "./conntexts/UserContext";
import LogIn from "./pages/LogIn";
import NotFound from "./pages/NotFound";
import DashboardLayout from "./layouts/dashboard/Layout";
import ProtectedRoute from "./utils/ProtectedRoute";
import NotAuthorized from "./pages/NotAuthorized";
import Bar from "./layouts/Bar";
import StartPage from "./pages/StartPage";

function App() {
    return (

        <Router>
            <UserProvider>
                <ThemeProvider theme={CustomThemeOptions}>
                    <div className="App">
                        <Bar/>
                        <div className="content">
                            <Routes>
                                <Route path="/login" element={<LogIn/>}/>
                                <Route element={<ProtectedRoute requiredRole='admin'/>}>
                                    <Route element={<DashboardLayout/>}>
                                        <Route path="/user" element={<NotFound/>}/>
                                        <Route path="/settings" element={<NotFound/>}/>
                                        <Route path="/support" element={<NotFound/>}/>
                                        <Route path="/home" element={<MainPage/>}/>
                                    </Route>
                                </Route>
                                <Route path="/unauthorized" element={<NotAuthorized/>}/>
                                <Route path="/" element={<StartPage/>}/>
                            </Routes>
                        </div>
                    </div>
                </ThemeProvider>
            </UserProvider>
        </Router>

    );
}


export default App;
