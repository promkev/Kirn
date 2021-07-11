import { Box, Button, Divider, Grid, makeStyles, Typography } from '@material-ui/core';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Loading from '../../Components/Loading/Loading';
import LoginButton from '../../Components/LoginButton/LoginButton';
import appwrite from '../../Constants/Appwrite';
import CreateExecution from '../../Modules/CreateExecution';
import GetUserSession from '../../Modules/GetUserSession';
import JoinCourseObject from '../../Models/JoinCourseObject';

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
        height: '100%',
        top: '50px',
    },
    centered: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    content: {
        fontSize: 25,
    },
}))

interface FunctionResponse {

}

export default function JoinCourseRoute() {
    const classes = useStyles();
    const [step, setStep] = useState<number>(0)
    const [botResp, setBotResp] = useState<JoinCourseObject>()

    useEffect(() => {
        CreateExecution(courseName!, guildId!)
            .then((resp) => {
                console.log(resp)
                if (resp === undefined) {
                    setStep(2)
                } else {
                    setBotResp(resp)
                    if (resp.success == true) {
                        setStep(1)
                    }
                    else if (resp.code == 0) {
                        setStep(4)
                    }
                    else if (resp.code == 1) {
                        setStep(3)
                    }
                }
            }
            )
    }, [])

    let { guildId, courseName } = useParams<Record<string, string | undefined>>();

    function stepSwitch(arg: number) {
        switch (arg) {
            // Loading
            case 0:
                return (<div >
                    <Loading />
                    <br />
                    <Typography className={classes.content}>Working on adding you to the {courseName?.toLocaleUpperCase()} channel!</Typography>
                    <Typography className={classes.content}> This may take a few seconds. </Typography>
                </div>)
            // Success
            case 1:
                return (<div>
                    <Typography className={classes.content}>✅ Success! ✅</Typography>
                    <Typography className={classes.content}>🎉You have been added to the {courseName?.toLocaleUpperCase()} channel. 🎉</Typography>
                    <Typography className={classes.content}>You can now close this browser tab.</Typography>
                </div>)
            // Log in required
            case 2:
                return (<div>
                    <Typography className={classes.content}>
                        Please log in using Discord
                    </Typography>
                    <LoginButton />
                </div>)
            // Join server required
            case 3:
                return (<div>
                    <Typography className={classes.content}>
                        Please join the server using this invite link.
                    </Typography>
                    <Typography>
                        {botResp!.extra}
                    </Typography>
                    <Typography className={classes.content}>
                        Once you are done, click the button below.
                    </Typography>
                </div>)
            case 4:
                return (<div>
                    <Typography className={classes.content}>
                        Invalid guild ID.
                    </Typography>
                </div>)
            case 5:
                return (<div>
                    <Typography className={classes.content}>
                        ❌ An unknown error has occured. ❌
                    </Typography>
                </div>)
        }
    }

    return (

        <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight="100vh"
        >
            <div className={classes.root}>{stepSwitch(step)}
            </div>
        </Box>

    );
}
