import { makeStyles, Toolbar } from '@material-ui/core';
import LoginButton from '../LoginButton/LoginButton';
import AppBar from '@material-ui/core/AppBar';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1
    },
    loginButton: {
        marginLeft: "auto"
    }
}))

export default function NavigationBar() {
    const classes = useStyles();
    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar >
                    <LoginButton className={classes.loginButton} />
                </Toolbar>
            </AppBar>
        </div>

    );
}

