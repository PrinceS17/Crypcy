import React, { Component } from 'react'
import { Button, Checkbox, Form, Card, Image, Header, Icon } from 'semantic-ui-react'
import axios from 'axios'
import {Link} from 'react-router-dom'
import styles from './listView.css'
import Article from '../Article/Article.jsx'
import GeneralLayout from "../Layout/GeneralLayout.jsx"
class ListView extends Component{
    constructor(props){
        super(props);
        this.state = {
            collection: [],
            errorState: 0,
        };
        // this.giveForm = this.giveForm.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.fetchList = this.fetchList.bind(this);
    }

    fetchList(){
        // const tempURL = `http://127.0.0.1:8000/api/`;
        const tempURL = `http://34.216.221.19:8000/api/currency/`
        axios.get(tempURL).then(res=>{
            this.setState({
                collection: res.data,
            });
            console.log(res.data);
        })
    }
    componentDidMount(){
        this.fetchList();
    }
    async handleFormSubmit(event){
        this.setState({
            errorState: 0,
        });

        const postObj = {
            name: event.target.elements.name.value,
            logo: event.target.elements.logo.value,
        }
        await axios.post("http://127.0.0.1:8000/api/create/", postObj).then(res=>{
            this.fetchList();
            this.setState({
                errorState: 2,
            });
        }).catch((err)=>{
            this.setState({
                errorState: 1,
            });
        });;
        
    }


    // giveForm(){
    //     return (

    //         <Card>
    //         <Header as='h3'>
    //         Manually create a coin
    //         </Header>
    //         <Form onSubmit={this.handleFormSubmit}>
    //         <Form.Field>
    //           <label>Name</label>
    //           <input name = 'name' placeholder='Name' />
    //         </Form.Field>
    //         <Form.Field>
    //           <label>Logo</label>
    //           <input name = 'logo' placeholder='Logo' />
    //         </Form.Field>
    //         {/* <Form.Field>
    //           <Checkbox label='I agree to the Terms and Conditions' />
    //         </Form.Field> */}
    //         <Button type='submit'>Submit</Button>
    //       </Form>
    //       </Card>
    //     );
    // }


    render(){
        let errorMessage = this.state.errorState===1? "Input Unvalid":"";
        if(this.state.errorState===2)  errorMessage="Insert Successful";
        return(
            <Article data = {this.state.collection} detailURL = '../detail/' />
        );
    }
}

export default ListView;