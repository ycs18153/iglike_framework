import {Container, Form, Button} from 'react-bootstrap';
import { useState } from 'react';

import './AutoFollowComponent.css';


const AutoFollowComponent = () => {
    const [inputs, setInputs] = useState({});

    const showForm = () => {

        const handleChange = (event) => {
            const name = event.target.name;
            const value = event.target.value;
            setInputs(values => ({ ...values, [name]: value }))
        }

        const handleSubmit = (event) => {
            event.preventDefault();
            console.log(inputs);
        }

        return (
            
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>IG 帳號</Form.Label>
                <Form.Control type="email" name="username" value={inputs.username || ""} placeholder="輸入帳號" onChange={handleChange} />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>密碼</Form.Label>
                <Form.Control type="password" name="password" value={inputs.password || ""} placeholder="密碼" onChange={handleChange}  />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicTargetAccount">
                <Form.Label>根據哪個帳號的粉絲</Form.Label>
                <Form.Control type="txt" name="targetAccount" value={inputs.targetAccount || ""} onChange={handleChange}  />
            </Form.Group>

            
            <Form.Group className="mb-3" controlId="formBasicMaximumFollowAmount">
                <Form.Label>隨機追蹤數</Form.Label>
                <Form.Select name="maximumFollowAmount" value={inputs.maximumFollowAmount || ""} onChange={handleChange}>
                    <option value="0">0</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                    <option value="200">200</option>
                    <option value="300">300</option>
                </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicMinimumWaitingTime">
                <Form.Label>min隨機等待時間</Form.Label>
                <Form.Select name="minimumWaitingTime" value={inputs.minimumWaitingTime || ""} onChange={handleChange}>
                    <option value="0">0s</option>
                    <option value="5">5s</option>
                    <option value="10">10s</option>
                    <option value="15">15s</option>
                    <option value="20">20s</option>
                </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicMaximumWaitingTime">
                <Form.Label>max隨機等待時間</Form.Label>
                <Form.Select name="maximumWaitingTime" value={inputs.maximumWaitingTime || ""} onChange={handleChange}>
                    <option value="0">0s</option>
                    <option value="30">30s</option>
                    <option value="40">40s</option>
                    <option value="50">50s</option>
                    <option value="60">60s</option>
                </Form.Select>
            </Form.Group>

            <Button variant="primary" type="submit">
                Submit
            </Button>
        </Form>
        )
    }

    return (
        <Container className="p-3">
            <Container className="p-5 mb-4 bg-light rounded-3">
                <h1 className="header">自動追蹤功能頁面</h1>
                {showForm()}
            </Container>
        </Container>
    )
};

export default AutoFollowComponent;