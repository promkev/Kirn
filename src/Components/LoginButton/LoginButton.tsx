import { Button, ButtonProps } from '@material-ui/core'
import appwrite from '../../Constants/Appwrite';

export default function LoginButton(props: ButtonProps) {
    const { REACT_APP_OAUTH2_REDIRECT_SUCCESS, REACT_APP_OAUTH2_REDIRECT_FAILURE } = process.env
    function login() {
        appwrite.account.createOAuth2Session('discord', REACT_APP_OAUTH2_REDIRECT_SUCCESS, REACT_APP_OAUTH2_REDIRECT_FAILURE)
    }
    return (
        <Button {...props} variant="contained" color="secondary" onClick={login}>Log in with Discord</Button>
    );
}