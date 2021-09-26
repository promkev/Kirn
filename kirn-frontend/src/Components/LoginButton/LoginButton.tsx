import { Button, ButtonProps, makeStyles } from '@material-ui/core'
import appwrite from '../../Constants/Appwrite';
import GetUserSession from '../../Modules/GetUserSession';
import { useEffect, useState } from 'react';

const useStyles = makeStyles((theme) => ({
    root: {
        minHeight: '100%',
        maxHeight: '100%',
        flexGrow: 1,
    },
    left: {
        marginLeft: 'auto',
        flexDirection: 'row',
        display: 'flex',
    }
}))

export default function LoginButton(props: ButtonProps) {
    const [loggedIn, setLoggedIn] = useState<boolean>(false)
    const classes = useStyles();

    useEffect(() => {
        GetUserSession().then(resp => {
            if (resp.$id === "") {
                setLoggedIn(false)
            } else {
                setLoggedIn(true)
            }
        })
    }, [])

    function login() {
        appwrite.account.createOAuth2Session('discord', window.location.href, window.location.href)
    }

    function logout() {
        GetUserSession().then(resp => {
            console.log(resp)
            if (resp.$id === "") {
                setLoggedIn(false)
                console.log("User is logged out")
            } else {
                try {
                    appwrite.account.deleteSession('current')
                    window.location.reload()
                    setLoggedIn(false)
                } catch (error) {
                    console.log(error)
                    setLoggedIn(false)
                }
            }
        })
    }
    return (
        <Button {...props} variant="contained" color="secondary" onClick={() => { loggedIn ? logout() : login() }} className={classes.root}>{loggedIn ? "Log out" : "Log in to Discord"}</Button>
    );
}