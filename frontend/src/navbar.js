import React from 'react'
import { Link } from 'react-router-dom'

function NavBar() {
    return (
        <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/auth">Auth</Link></li>
            <li><Link to="/Unauth">Unauth</Link></li>
        </ul>
    );
}

export default NavBar;