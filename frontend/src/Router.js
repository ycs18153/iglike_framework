import {BrowserRouter, Route, Routes} from 'react-router-dom'

import App from "./App";
import AutoLikeComponent from "./component/ig_function/auto_like/AutoLikeComponent";

const Router = () => {
    return (
        <BrowserRouter>
            <Routes> 
                <Route path="/" element={<App/>} />
                <Route path="/auto-like" element={<AutoLikeComponent/>} />
            </Routes>
        </BrowserRouter>
    )
}

export default Router;