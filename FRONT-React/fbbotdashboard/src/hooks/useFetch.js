import {useState, useEffect} from 'react';
import {useAuth} from "../conntexts/UserContext";

export const API_HOST = 'https://3.20.227.39:8000'
export const AUTH_HOST = 'https://3.20.227.39:8080'

export const useFetchCars = (url, setCars) => {
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const {token} = useAuth();

    useEffect(() => {
        fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json'
            }
        })
            .then(response => {
                if (!response.ok) {
                    // error coming back from server
                    throw Error('could not fetch the data for that resource');
                }
                return response.json();
            })
            .then(data => {
                setIsLoading(false);

                data = [...data.map(car => {
                    car.date = new Date(car.date);
                    car.new = false;
                    return car;
                })]

                setCars(data);
                setError(null);
            })
            .catch(err => {
                setIsLoading(false);
                setError(err.message);
            })
    }, [url])

    return [isLoading, error];
}


export const useFetchRefreshCars = (url, cars, setCars, actionDone, setActionDone) => {
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const {token} = useAuth();

    useEffect(() => {

        if (actionDone) {
            fetch(url, {
                headers: {
                    'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    if (!response.ok) {
                        // error coming back from server
                        throw Error('could not fetch the data for that resource');
                    }
                    return response.json();
                })
                .then(data => {
                    setIsLoading(false);

                    data = [...data.map(new_car => {
                        new_car.date = new Date(new_car.date);
                        new_car.new = cars.some(car => car.id === new_car.id);
                        return new_car;
                    })]


                    setCars(data);

                    setActionDone(false);
                    setError(null);
                })
                .catch(err => {
                    setIsLoading(false);
                    setError(err.message);
                })
        }
    }, [url, actionDone])

    return [isLoading, error];
}


export const useFetchPutCars = (url, setActionDone) => {
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const {token} = useAuth();

    useEffect(() => {
        if (url) {
            fetch(url, {
                method: 'PUT', headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }

            })
                .then(response => {
                    if (!response.ok) {
                        // error coming back from server
                        throw Error('Could not update car');
                    }
                    setActionDone(true);
                    return response.json();
                })
                .then(() => {
                    setError(null);
                })
                .catch(err => {
                    setActionDone(false);
                    setIsLoading(false);
                    setError(err.message);
                })
        }
    }, [url])

    return [isLoading, error];
}

export const useFetchGetCars = (refresh, setRefresh) => {
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const {token} = useAuth();

    useEffect(() => {
        if (refresh) {
            fetch(`${API_HOST}/list-new/list-new`, {
                method: 'GET', headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
                .then(response => {
                    if (!response.ok) {
                        // error coming back from server
                        throw Error('Could not update car');
                    }
                    setRefresh(false);
                    return response.json();
                })
                .then(() => {
                    setError(null);

                })
                .catch(err => {
                    setRefresh(false);
                    setIsLoading(false);
                    setError(err.message);
                })
        }
    }, [refresh])

    return [isLoading, error];
}
