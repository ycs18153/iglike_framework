import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

import './AuthComponent.css';

const Auth = () => (
    <Container className="p-3">
        <Container className="p-5 mb-4 bg-light rounded-3">
            <h2 className="header">Welcome To IG Like system</h2>
            <Container className='row mt-1'>
                <Link to="/auto-like">
                    <Button>自動按讚</Button>
                </Link>
            </Container>
            <Container className='row mt-1'>
                <Link to="/auto-follow">
                    <Button>自動追蹤</Button>
                </Link>
            </Container>
            <Container className='row mt-1'>
                <Link to="/auto-dm">
                    <Button>自動私訊</Button>
                </Link>
            </Container>
            <Container className='row mt-1'>
                <Link to="/auto-unfollow">
                    <Button>自動退追</Button>
                </Link>
            </Container>
        </Container>
    </Container>
);

export default Auth;
