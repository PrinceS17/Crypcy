import React, { Component } from 'react'
import axios from "axios";
import {Button, Form, Card, Image, Header, Icon} from 'semantic-ui-react';
import {Link} from 'react-router-dom'
import styles from './detailView.css'
class DetailView extends Component{
    constructor(props){
        super(props);
        this.state = {
            detailData: [],   
            errorState: 0,
            deleted: 1,

        };
        this.handleDelete = this.handleDelete.bind(this);
        this.fetchDetail = this.fetchDetail.bind(this);
        this.giveForm = this.giveForm.bind(this);
        this.handelFormSubmit = this.handelFormSubmit.bind(this);
        this.detailCard = this.detailCard.bind(this);
        

    }

    fetchDetail(){
        const detailID = this.props.match.params.ix;
        console.log("Getting Data");
        axios.get(`http://127.0.0.1:8000/api/${detailID}`).then((res)=>{

            this.setState({
                detailData: res.data,
                deleted: 0,

            });
        }).catch(err=>{
            console.log('Not Found');
            this.setState({
                deleted: 1,
                detailData: [],
            });
        });
        
    }
    componentDidMount(){
        this.fetchDetail();
    }

    handelFormSubmit(event){
        this.setState({
            errorState: 0,
        });

        const postObj = {
            name: event.target.elements.name.value,
            logo: event.target.elements.logo.value,
        }
        const detailID = this.props.match.params.ix;
        axios.put(`http://127.0.0.1:8000/api/${detailID}/update/`, postObj).then(res=>{
            this.fetchDetail();
            this.setState({
                errorState: 2,
            });
        }).catch((err)=>{
            this.setState({
                errorState: 1,
            });
        });;
        
    }

    detailCard(){
        console.log(this.state.detailData.time);
        let timeSlotData = "";
        if(this.state.detailData.time!==undefined){
            timeSlotData = this.state.detailData.time.map((ts) =>{
                return(
                    <div>{ts}</div>
                );
            });
            return(
                <Card>
                    
                <Card.Content>
                <Card.Header><Image src={this.state.detailData.logo} />{this.state.detailData.name}</Card.Header>
                <Card.Meta>
                        {`Currency ID: #${this.state.detailData.id}`}
                    </Card.Meta>
                </Card.Content>
                <Card.Content extra>
                TimeSlot: <br/> {timeSlotData}
                </Card.Content>
                </Card>
            );
        }

        return (
            <Card>
                    
            <Card.Content>
            <Card.Header>CryptoCurrency Not Found</Card.Header>
 
            </Card.Content>
            </Card>
        );

    }

    giveForm(){
        return (
            <Card>
            <Header as='h3'>
            Manually update coin
            </Header>
            <Form onSubmit={this.handelFormSubmit}>
            <Form.Field>
              <label>Name</label>
              <input name = 'name' placeholder='Name' />
            </Form.Field>
            <Form.Field>
              <label>Logo</label>
              <input name = 'logo' placeholder='Logo' />
            </Form.Field>
            {/* <Form.Field>
              <Checkbox label='I agree to the Terms and Conditions' />
            </Form.Field> */}
            <Button type='submit'>Submit</Button>
          </Form>
          </Card>
        );
    }

    handleDelete(){
        const detailID = this.props.match.params.ix;
        const tempURL = `http://127.0.0.1:8000/api/${detailID}/delete`;
        console.log(tempURL);
        axios.delete(tempURL).then((res)=>{
            this.fetchDetail();
            this.setState({
                deleted: 1,
            });
        });
    }

    render(){
        
        let errorMessage = this.state.errorState===1? "Update Operation Unvalid":"";
        if(this.state.errorState===2)  errorMessage="Insert Successful";
        return (
            <div className = 'Detail-Container'>
                <Header as = 'h2' textAlign = 'left'>
                <Icon name='currency' circular />
                Detail of Currency
                </Header>
                {/* <div>ID: {this.props.match.params.ix} </div>
                <div>Data: {JSON.stringify(this.state.detailData)}</div> */}
                {this.detailCard()}<br />

                {this.giveForm()}<br />
                {errorMessage}<br />
                <Button  onClick={this.handleDelete}>
                    Delete
                </Button>

                <Link to ="../">
                <Button >
                    To Homepage
                </Button>
                </Link>
            </div>
            
        );
    }
}

export default DetailView;