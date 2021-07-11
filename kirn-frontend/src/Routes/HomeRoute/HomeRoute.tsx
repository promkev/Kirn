import { makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1
    },
}))

export default function HomeRoute() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
        </div>
    );
}

