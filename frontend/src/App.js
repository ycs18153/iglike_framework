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
            sessionStorage.setItem("liff_user_id", 'U71104f51176a5b84c2fe5555cb88275f')
            // sessionStorage.setItem("liff_user_id", liff.getDecodedIDToken()['sub'])
        }).then(()=>{
            axios('/iglike/' + sessionStorage.getItem('liff_user_id'))
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