import {Container, Form, Button} from 'react-bootstrap';
import { useState } from 'react';
import axios from 'axios';

import './AutoLikeComponent.css';


const AutoLikeComponent = () => {
    const [inputs, setInputs] = useState({});
    const liff_user_id = sessionStorage.getItem('liff_user_id');

    const showForm = () => {

        const handleChange = (event) => {
            const name = event.target.name;
            const value = event.target.value;
            setInputs(values => ({ ...values, [name]: value }))
            setInputs(values => ({ ...values, ['uid']: liff_user_id }))
        }

        const handleSubmit = (event) => {
            event.preventDefault();
            console.log(inputs);
            // @router.get("/autolike/{uid}/{account}/{password}/{minWaitTime}/{maxWaitTime}/{hashtag}/{maxLike}", response_description="exec auto lilke")
            axios('/iglike/autolike/' 
                + inputs['uid'] + "/"
                + inputs['username'] + "/"
                + inputs['password'] + "/"
                + inputs['minimumWaitingTime'] + "/"
                + inputs['maximumWaitingTime'] + "/"
                + inputs['hashtag'] + "/"
                + inputs['maximumLikeAmount'])
            .then((response) => {
                if (response['data'] === 'op') {
                    window.alert('程式執行中，請稍候至查詢頁面查看結果')
                } else {
                    window.alert('程式錯誤。')
                }
            })
        }

        return (
            
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>IG 帳號</Form.Label>
                <Form.Control type="txt" name="username" value={inputs.username || ""} placeholder="輸入帳號" onChange={handleChange} />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>密碼</Form.Label>
                <Form.Control type="password" name="password" value={inputs.password || ""} placeholder="密碼" onChange={handleChange}  />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicHashtag">
                <Form.Label>Hashtag</Form.Label>
                <Form.Control type="txt" name="hashtag" value={inputs.hashtag || ""} placeholder="Hashtag" onChange={handleChange}  />
            </Form.Group>

            
            <Form.Group className="mb-3" controlId="formBasicMaximumLikeAmount">
                <Form.Label>Max讚數</Form.Label>
                <Form.Select name="maximumLikeAmount" value={inputs.maximumLikeAmount || ""} onChange={handleChange}>
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
                    <option value="">請選擇</option>
                    <option value="1">1s</option>
                    <option value="2">2s</option>
                    <option value="3">3s</option>
                    <option value="4">4s</option>
                    <option value="5">5s</option>
                </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicMaximumWaitingTime">
                <Form.Label>max隨機等待時間</Form.Label>
                <Form.Select name="maximumWaitingTime" value={inputs.maximumWaitingTime || ""} onChange={handleChange}>
                    <option value="">請選擇</option>
                    <option value="6">6s</option>
                    <option value="7">7s</option>
                    <option value="8">8s</option>
                    <option value="9">9s</option>
                    <option value="10">10s</option>
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
                <h1 className="header">自動按讚功能頁面</h1>
                {showForm()}
            </Container>
        </Container>
    )
};

export default AutoLikeComponent;
