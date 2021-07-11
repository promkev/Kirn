import { CircularProgress, makeStyles } from '@material-ui/core';
import { useRef } from 'react';

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        height: '100%',
    },
    circularprogress: {
        top: '50%'
    }
}))

export default function Loading() {
    const classes = useStyles();
    const parentRef = useRef<HTMLDivElement>(null);

    return (
        <div ref={parentRef} className={classes.root} >
            <CircularProgress className={classes.circularprogress} color="secondary" size={'10%'} />
        </div>

    );
}

