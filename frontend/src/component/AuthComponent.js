import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

import AutoLikeComponent from './ig_function/auto_like/AutoLikeComponent'

import './AuthComponent.css';

const showAutoLikePage = () => {
    return <AutoLikeComponent></AutoLikeComponent>
};

const Auth = () => (
    <Container className="p-3">
        <Container className="p-5 mb-4 bg-light rounded-3">
        <h2 className="header">Welcome To IG Like system</h2>
            <Container className='row mt-1'>
            <Link to="/auto-like">
                <Button onClick="/auto-like">自動按讚</Button>
            </Link>
            </Container>
            <Container className='row mt-1'>
                <Link to="/auto-follow">
                    <Button onClick="/auto-follow">自動追蹤</Button>
                </Link>
            </Container>
        </Container>
    </Container>
);

export default Auth;
