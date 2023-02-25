import {BrowserRouter, Route, Routes} from 'react-router-dom'

import App from "./App";
import AutoLikeComponent from "./component/ig_function/auto_like/AutoLikeComponent";
import AutoFollowComponent from "./component/ig_function/auto_follow/AutoFollowComponent";
import AutoDmComponent from "./component/ig_function/auto_dm/AutoDmComponent";
import AutoUnfollowComponent from "./component/ig_function/auto-unfollow/AutoUnfollowComponent";

const Router = () => {
    return (
        <BrowserRouter>
            <Routes> 
                <Route path="/" element={<App/>} />
                <Route path="/auto-like" element={<AutoLikeComponent/>} />
                <Route path="/auto-follow" element={<AutoFollowComponent/>} />
                <Route path="/auto-dm" element={<AutoDmComponent/>} />
                <Route path="/auto-unfollow" element={<AutoUnfollowComponent/>} />
            </Routes>
        </BrowserRouter>
    )
}

export default Router;