import { CircularProgress, makeStyles, Toolbar } from '@material-ui/core';
import LoginButton from '../LoginButton/LoginButton';
import AppBar from '@material-ui/core/AppBar';
import { useEffect, useRef, useState } from 'react';

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
    const [parentSize, setParentSize] = useState(0);
    const parentRef = useRef<HTMLDivElement>(null);


    useEffect(() => {
        const { clientHeight, clientWidth } = parentRef.current!;

        setParentSize(Math.min(clientHeight, clientWidth));
    }, []);

    return (
        <div ref={parentRef} className={classes.root} >
            <CircularProgress className={classes.circularprogress} color="secondary" size={'10%'} />
        </div>

    );
}

