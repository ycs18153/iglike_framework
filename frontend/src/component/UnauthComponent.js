import Container from 'react-bootstrap/Container';

import './UnauthComponent.css';

const Unauth = () => (
    <Container className="p-3">
        <Container className="p-5 mb-4 bg-light rounded-3">
        <h1 className="header">您的帳號尚未授權</h1>
        <h2 className="header">請回到 Line Bot 完成授權並再次使用本服務。</h2>
        </Container>
    </Container>
);

export default Unauth;
