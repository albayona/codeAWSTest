import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

import {
    Button, CardActionArea, CardActions, Chip, Divider, Grid, ImageList, ImageListItem, Stack, styled
} from '@mui/material';
import Box from "@mui/material/Box";

export default function DetailCard({car}) {

    const Item = styled(Box)(({theme}) => ({
        padding: theme.spacing(0), textAlign: 'center', color: theme.palette.text.secondary,
    }));

    const attributes = [
        {label: `Price: ${car.price}`, variant: "outlined"},
        {label: `Model: ${car.model}`, variant: "outlined"},
        {label: `Year: ${car.year}`, variant: "outlined"},
        {label: `Place: ${car.place}`, variant: "outlined"},
        {label: `Miles: ${car.miles}`, variant: "outlined"},
        {label: `Date: ${car.date.toLocaleDateString()}`, variant: "outlined"},
        {label: `Score: ${car.score}`, variant: "outlined"},
    ];


    const Root = styled('div')(({ theme }) => ({
        width: '100%',
        ...theme.typography.body2,
        color: theme.palette.text.secondary,
        '& > :not(style) ~ :not(style)': {
            marginTop: theme.spacing(2),
        },
    }));



    return (<Card sx={{maxWidth: '100%', maxHeight: '100%'}}>
        <CardActionArea>

        </CardActionArea>
        <CardContent>

            <Grid container spacing={2}>
                <Grid item xs={7}>
                    <ImageList sx={{width: '100%', maxHeight: '450px', overflowY: 'auto'}} cols={3} rowHeight={200}>
                        {car.images.map((item) => (
                            <ImageListItem key={item}>
                                <img
                                    srcSet={`${item}`}
                                    src={`${item}`}
                                    alt='img'
                                    loading="lazy"
                                />
                            </ImageListItem>
                        ))}
                    </ImageList>

                </Grid>
                <Grid item xs={5}>
                    <Stack spacing={1} sx={{width: '100%', maxHeight: '450px', overflowY: 'auto'}}>
                        <Root>
                            <Divider>
                                <Chip label={
                                    <Typography variant="h6" gutterBottom>
                                        Main Attributes
                                    </Typography>

                                } size="medium" />
                            </Divider>

                            <Item>
                                {attributes.map((attr, index) => (
                                    <Chip key={index} label={attr.label} style={{marginRight: '5px', marginBottom: '5px'}}/>
                                ))}
                            </Item>

                            <Divider>
                                <Chip label={
                                    <Typography variant="h6" gutterBottom>
                                        Secondary Attributes
                                    </Typography>

                                } size="medium" />
                            </Divider>

                            <Item>
                                {car.about.map((attr, index) => (
                                    <Chip key={index} label={attr} style={{marginRight: '5px', marginBottom: '5px'}}/>
                                ))}
                            </Item>

                            <Divider>
                                <Chip label={
                                    <Typography variant="h6" gutterBottom>
                                        Seller Attributes
                                    </Typography>

                                } size="medium" />
                            </Divider>

                            <Item>
                                {car.seller.map((attr, index) => (
                                    <Chip key={index} label={attr} style={{marginRight: '5px', marginBottom: '5px'}}/>
                                ))}
                            </Item>

                        </Root>

                    </Stack>
                </Grid>

            </Grid>


            <Typography gutterBottom variant="h5" component="div">
                {car.model}
            </Typography>
            <Typography variant="caption" color="text.secondary">
                {car.description}
            </Typography>


        </CardContent>
        <CardActions>
            <Button size="small" color="primary" href={"https://www.facebook.com/marketplace/item/" + car.link}>
                View
            </Button>
        </CardActions>
    </Card>);
}