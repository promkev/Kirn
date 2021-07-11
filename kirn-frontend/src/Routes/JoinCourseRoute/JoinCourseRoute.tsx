import { Box, Button, makeStyles, Typography } from '@material-ui/core';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Loading from '../../Components/Loading/Loading';
import LoginButton from '../../Components/LoginButton/LoginButton';
import CreateExecution from '../../Modules/CreateExecution';
import JoinCourseObject from '../../Models/JoinCourseObject';
import { openInNewTab } from '../../Modules/OpenInNewTab';

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
        fontSize: 26,
    },
    mediumcontent: {
        fontSize: 20,
    },
    smallcontent: {
        fontSize: 14,
    },
    link: {
        color: '#03e3fc'
    }
}))

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
                    if (resp.success === true) {
                        setStep(1)
                    }
                    else if (resp.code === 0) {
                        setStep(4)
                    }
                    else if (resp.code === 1) {
                        setStep(3)
                    }
                }
            }
            )
        // eslint-disable-next-line
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
                    <Typography className={classes.mediumcontent}>
                        {courseName?.toLocaleUpperCase()} is a channel on a Discord server using Kirn for course channel management.
                    </Typography>
                    <Typography className={classes.mediumcontent}>
                        You must first log into Discord, and join the server before the bot can add you to the course channel.
                    </Typography>
                    <br />
                    <Typography className={classes.content}>
                        Please log in to Discord to continue.
                    </Typography>
                    <LoginButton />
                </div>)
            // Join server required
            case 3:
                return (<div>
                    <Typography className={classes.content}>
                        Please join the Discord server, and come back to this page.
                    </Typography>
                    <Typography className={classes.smallcontent}>
                        (If the button does not work: <a href={botResp!.extra} target="_blank" rel="noopener noreferrer" className={classes.link}>{botResp!.extra}</a>)
                    </Typography>
                    <Typography>
                        <Button onClick={() => openInNewTab(botResp!.extra)} variant="contained" color="secondary">
                            Join Discord Server
                        </Button>
                    </Typography>

                    <br />
                    <Typography className={classes.content}>
                        Once you are done, click the button below.
                    </Typography>
                    <Button onClick={() => window.location.reload(true)} variant="contained" color="primary">
                        Continue
                    </Button>

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

