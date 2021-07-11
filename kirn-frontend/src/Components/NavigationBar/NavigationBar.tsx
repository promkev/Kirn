import { Button, makeStyles, Toolbar, Typography } from '@material-ui/core';
import LoginButton from '../LoginButton/LoginButton';
import AppBar from '@material-ui/core/AppBar';
import { useEffect, useState } from 'react';
import GetUserSession from '../../Modules/GetUserSession';
import { openInNewTab } from '../../Modules/OpenInNewTab';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    left: {
        marginLeft: 'auto',
        flexDirection: 'row',
        display: 'flex',
    },
    button: {
        marginRight: '2vh',
    }
}))

export default function NavigationBar() {
    const classes = useStyles();
    const [name, setName] = useState<string>("")


    useEffect(() => {
        GetUserSession().then(resp => {
            if (resp.$id === "") {
                setName("Not logged in")
            } else {
                setName("Logged in as " + resp.name)
            }
        })
    }, [])

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar >
                    <Typography>{name}</Typography>
                    <div className={classes.left}>
                        <Button className={classes.button} variant="contained" onClick={() => openInNewTab('https://github.com/GryPr/Kirn')}>Source Code</Button>
                        <LoginButton />
                    </div>
                </Toolbar>
            </AppBar>
        </div>

    );
}

