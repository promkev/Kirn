import { Button, ButtonProps } from '@material-ui/core'
import appwrite from '../../Constants/Appwrite';
import GetUserSession from '../../Modules/GetUserSession';
import { useEffect, useState } from 'react';

export default function LoginButton(props: ButtonProps) {
    const { REACT_APP_OAUTH2_REDIRECT_SUCCESS, REACT_APP_OAUTH2_REDIRECT_FAILURE } = process.env
    const [loggedIn, setLoggedIn] = useState<boolean>(false)
    const [loaded, setLoaded] = useState<boolean>(false)

    useEffect(() => {
        GetUserSession().then(resp => {
            if (resp.$id === "") {
                setLoggedIn(false)
            } else {
                setLoggedIn(true)
            }
        }).then(() => setLoaded(true))
    }, [])

    function login() {
        appwrite.account.createOAuth2Session('discord', REACT_APP_OAUTH2_REDIRECT_SUCCESS, REACT_APP_OAUTH2_REDIRECT_FAILURE)
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
                    setLoggedIn(false)
                } catch (error) {
                    console.log(error)
                    setLoggedIn(false)
                }
            }
        })
    }
    return (
        <div>
            {loaded ? [loggedIn ? <Button {...props} variant="contained" color="secondary" onClick={logout}>Logout</Button> : <Button {...props} variant="contained" color="secondary" onClick={login}>Log in with Discord</Button>
            ] : ""
            }
        </div>
    );
}