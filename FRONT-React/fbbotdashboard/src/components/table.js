import * as React from 'react';
import Box from '@mui/material/Box';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import FavoriteIcon from '@mui/icons-material/Favorite';
import VisibilityIcon from '@mui/icons-material/Visibility';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import CircleNotificationsIcon from '@mui/icons-material/CircleNotifications';
import {
    GridToolbar,
    DataGrid,
    GridActionsCellItem,

} from '@mui/x-data-grid';
import {useEffect, useState} from "react";
import {API_HOST, useFetchCars, useFetchGetCars, useFetchPutCars, useFetchRefreshCars} from "../hooks/useFetch";
import DetailCard from "./detail";
import {Button, Modal} from "@mui/material";


const modalStyle = {
    position: 'absolute',
    top: '2%',  /* Set left to 50% */
    left: '50%',  /* Set left to 50% */
    width: '75%',  /* Make width 90% of the container */
    transform: 'translateX(-50%)',
    maxHeight: '800px',
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

function extractID(message) {
    const prefix = "data: ";
    if (message.startsWith(prefix)) {
        const rawData = message.slice(prefix.length).trim();
        if (rawData.startsWith("b'") && rawData.endsWith("'")) {
            const data = rawData.slice(2, -1);
            const number = parseInt(data, 10);
            if (!isNaN(number)) {
                return number;
            } else {
                return null;
            }
        } else {
            return null;
        }
    } else {
        return null;
    }
}

// Example usage
try {
    const message = "data: b'117'";
    const extractedNumber = extractID(message);
    console.log('Extracted Number:', extractedNumber);  // Output: 117
} catch (error) {
    console.error(error.message);
}


export default function FullFeaturedCrudGrid({url, type}) {
    const [cars, setCars] = useState([]);
    const [selectedCar, setSelectedCar] = useState({});
    const [actionURl, setActionURL] = useState('');
    const [refreshAction, setRefreshAction] = useState(false);
    const [actionDone, setActionDone] = useState(false);
    const [isLoading, error] = useFetchCars(url, setCars);
    const [refreshLoading, refreshError] = useFetchRefreshCars(url, cars, setCars, actionDone, setActionDone);
    const [putLoading, putError] = useFetchPutCars(actionURl, setActionDone);
    const [getLoading, gettError] = useFetchGetCars(refreshAction, setRefreshAction);
    const [newCars, setNewCars] = useState([]);


    const [open, setOpen] = React.useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);


    useEffect(() => {
        if (type !== "New") return

        const es = new EventSource(`${API_HOST}/subscribe/subscribe/user`);

        es.onopen = () => console.log(">>> Connection opened!");

        es.onerror = (e) => console.log("ERROR!", e);

        es.onmessage = (e) => {
            console.log(">>>", e.data);
            if (e.data.startsWith('data')) {
                setActionDone(true);
            }
        };

        return () => es.close();
    }, []);


    const handleLikeClick = (id) => () => {
        setActionURL(`${API_HOST}/like/like/` + id);
    };


    const handleDislikeClick = (id) => () => {
        setActionURL(`${API_HOST}/unlike/unlike/` + id);
    };

    const handleArchiveClick = (id) => () => {
        setActionURL(`${API_HOST}/see/see/` + id);
    };

    const handleUnarchiveClick = (id) => () => {
        setActionURL(`${API_HOST}/unsee/unsee/` + id);
    };

    const handleInfoClick = (id) => () => {
        setSelectedCar(cars.find(car => car.id === id));
        console.log(cars.find(car => car.id === id));
        handleOpen();
    };


    const processRowUpdate = (newRow) => {
        const updatedRow = {...newRow, isNew: false};
        setCars(cars.map((row) => (row.id === newRow.id ? updatedRow : row)));
        return updatedRow;
    };

    let button = null;
    let button2 = null;

    function archiveAll() {
        setActionURL(`${API_HOST}/see-all/see-all/`);
    }

    function emptyFavorites() {
        setActionURL(`${API_HOST}/empty-fav/empty-fav/`);
    }

    function refresh() {
        setRefreshAction(true);
    }

    if (type === "New") {
        button = <Button onClick={archiveAll} variant="contained">Archive all</Button>
    } else if (type === "Favs") {
        button = <Button onClick={emptyFavorites} variant="contained">Empty favorites</Button>
    }

    function isCarNewById(carId) {
        // Find the car object with the matching ID
        const car = cars.find(car => car.id === carId);

        // Check if the car exists and has the 'new' property set to true
        if (car && car.new === true) {
            return true;
        } else {
            return false;
        }
    }


    const columns = [

        {
            field: 'actions',
            type: 'actions',
            headerName: 'Actions',
            width: 230,
            cellClassName: 'actions',
            getActions: ({id}) => {
                return [

                    <GridActionsCellItem
                        icon={<CircleNotificationsIcon/>}
                        label="New"
                        onClick={handleInfoClick(id)}
                        color="primary"
                        disabled={isCarNewById(id)}
                    />,

                    <GridActionsCellItem
                        icon={<InfoOutlinedIcon/>}
                        label="Unarchive"
                        onClick={handleInfoClick(id)}
                        color="inherit"

                    />,


                    <GridActionsCellItem
                        icon={<FavoriteIcon/>}
                        label="Like"
                        className="textPrimary"
                        onClick={handleLikeClick(id)}
                        color="inherit"
                    />,
                    <GridActionsCellItem
                        icon={<ThumbDownIcon/>}
                        label="Discard"
                        onClick={handleDislikeClick(id)}
                        color="inherit"

                    />,

                    <GridActionsCellItem
                        icon={<VisibilityOffIcon/>}
                        label="Archive"
                        onClick={handleArchiveClick(id)}
                        color="inherit"
                        disabled={type === "Old"}
                    />,


                    <GridActionsCellItem
                        icon={<VisibilityIcon/>}
                        label="Unarchive"
                        onClick={handleUnarchiveClick(id)}
                        color="inherit"
                        disabled={type === "New"}
                    />,

                ];
            },
        },

        {
            field: 'score',
            headerName: 'Score',
            type: 'number',
            width: 100,
            editable: true,
        },
        {
            field: 'price',
            headerName: 'Price',
            type: 'number',
            width: 100,
            editable: true,
        },

        {
            field: 'miles',
            headerName: 'Miles',
            type: 'number',
            width: 100,
            editable: true,
        },

        {
            field: 'year',
            headerName: 'Year',
            type: 'number',
            width: 100,
            editable: true,
        },
        {
            field: 'model',
            headerName: 'Model',
            width: 150,
            editable: true,
        },

        {
            field: 'date',
            headerName: 'Date',
            type: 'date',
            width: 150,
            editable: true,
        },

        {
            field: 'place',
            headerName: 'Place',
            width: 150,
            editable: true,
        },


        {
            field: 'description',
            headerName: 'Description',
            width: 200,
            editable: true,
        },


    ];

    return (
        <Box
            sx={{
                height: 800,
                width: '100%',
                '& .actions': {
                    color: 'text.secondary',
                },
                '& .textPrimary': {
                    color: 'text.primary',
                },
            }}
        >
            {button}
            {button2}
            <Modal
                open={open}
                onClose={handleClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={modalStyle}>
                    {Object.keys(selectedCar).length === 0 ? null : <DetailCard car={selectedCar}></DetailCard>}
                </Box>
            </Modal>

            <DataGrid
                rows={cars}
                columns={columns}
                editMode="row"
                processRowUpdate={processRowUpdate}
                slots={{
                    toolbar: GridToolbar,
                }}
            />
        </Box>
    );
}