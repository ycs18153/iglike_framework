import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useLiff } from 'react-liff';

import Auth from "./component/AuthComponent";
import Unauth from './component/UnauthComponent';

const App = () => {
    const [component, setComponent] = useState('');
    const { error, isLoggedIn, isReady, liff } = useLiff();

    useEffect(() => {
        if (!isLoggedIn) return;

    }, [liff, isLoggedIn]);

    const showComponent = () => {
        liff.getProfile()
        .then((profile)=>{
            return profile.userId
        }).then((userId)=>{
            axios('/iglike/' + userId)
                .then((response) => {
                    if (response['data'] === '-1') {
                        setComponent(<Unauth></Unauth>)
                    } else {
                        setComponent(<Auth></Auth>)
                    }
                })
        })
        
        return component
    }

    const showLiffLogin = () => {
        if (error) return <p>Something is wrong.</p>;
        if (!isReady) return <p>Loading...</p>;

        if (!isLoggedIn) {
            liff.login()
        }

        if (isLoggedIn) {
            return showComponent()
        }
    };

    return (
        <div className="App">
            {showLiffLogin()}
        </div>
    );
};

export default App;