import { makeStyles, Toolbar, Typography } from '@material-ui/core';
import LoginButton from '../LoginButton/LoginButton';
import AppBar from '@material-ui/core/AppBar';
import { useEffect, useState } from 'react';
import GetUserSession from '../../Modules/GetUserSession';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    left: {
        marginLeft: 'auto',
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
                setName(resp.name)
            }
        })
    }, [])

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar >
                    <Typography>Logged in as {name}</Typography>
                    <div className={classes.left}>
                        <LoginButton />
                    </div>
                </Toolbar>
            </AppBar>
        </div>

    );
}

