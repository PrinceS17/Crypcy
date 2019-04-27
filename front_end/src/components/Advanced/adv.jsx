import React, { Component } from 'react'
import axios from "axios";
import {Button, Form, Card, Image, Header, Icon} from 'semantic-ui-react';
import {Link} from 'react-router-dom'
import styles from './adv.css'
class Adv extends Component{
    constructor(props){
        super(props);
        this.state = {
            adv1Data: [],
            adv2Data: [],

        };
        // this.fetchDetail = this.fetchDetail.bind(this);
        this.giveForm = this.giveForm.bind(this);
        this.handelFormSubmit = this.handelFormSubmit.bind(this);
        this.advCard = this.advCard.bind(this);
        // this.detailCard = this.detailCard.bind(this);
        

    }

    // fetchDetail(){
    //     const detailID = this.props.match.params.ix;
    //     console.log("Getting Data");
    //     axios.get(`http://127.0.0.1:8000/api/${detailID}`).then((res)=>{

    //         this.setState({
    //             detailData: res.data,
    //             deleted: 0,

    //         });
    //     }).catch(err=>{
    //         console.log('Not Found');
    //         this.setState({
    //             deleted: 1,
    //             detailData: [],
    //         });
    //     });
        
    // }
    // componentDidMount(){
    //     this.fetchDetail();
    // }



    // detailCard(){
    //     console.log(this.state.detailData.time);
    //     let timeSlotData = "";
    //     if(this.state.detailData.time!==undefined){
    //         timeSlotData = this.state.detailData.time.map((ts) =>{
    //             return(
    //                 <div>{ts}</div>
    //             );
    //         });
    //         return(
    //             <Card>
                    
    //             <Card.Content>
    //             <Card.Header><Image src={this.state.detailData.logo} />{this.state.detailData.name}</Card.Header>
    //             <Card.Meta>
    //                     {`Currency ID: #${this.state.detailData.id}`}
    //                 </Card.Meta>
    //             </Card.Content>
    //             <Card.Content extra>
    //             TimeSlot: <br/> {timeSlotData}
    //             </Card.Content>
    //             </Card>
    //         );
    //     }

    //     return (
    //         <Card>
                    
    //         <Card.Content>
    //         <Card.Header>CryptoCurrency Not Found</Card.Header>
 
    //         </Card.Content>
    //         </Card>
    //     );

    // }

    advCard(cardType){

        
        if(cardType ===1){
            let cardEntries = this.state.adv1Data.map((item,index)=>{
                return (
                    <Card>
                    <Card.Content>
                    <Card.Header><Image src={item.logo} />{item.name}</Card.Header>
                    <Card.Meta>
                            {`Currency ID: #${item.id}`}
                        </Card.Meta>
                    </Card.Content>
                    <Card.Content extra>
                    Price: <br/> {item.price}
                    </Card.Content>
                    </Card>
                )

            });
            return cardEntries;
        }
        else{
            let cardEntries = this.state.adv2Data.map((item,index)=>{
                return (
                    <Card>
                    <Card.Content>
                    <Card.Header><Image src={item.logo} />{item.name}</Card.Header>
                    <Card.Meta>
                            {`Currency ID: #${item.id}`}
                        </Card.Meta>
                    </Card.Content>
                    <Card.Content extra>
                    Utility: <br/> {item.utility}
                    </Card.Content>
                    </Card>
                )
    
            });
            return cardEntries;
        }        
    
    }
    giveForm(formType){

        if(formType===1){
            return (
                <Card>
                <Header as='h3'>
                Advanced Function 1 Parameter
                </Header>
                <Form className="adv1" onSubmit={this.handelFormSubmit}>
                <Form.Field>
                  <label>Price 1</label>
                  <input name = 'param1' placeholder='Price 1' />
                </Form.Field>
                <Form.Field>
                  <label>Price 2</label>
                  <input name = 'param2' placeholder='Price 2' />
                </Form.Field>
                {/* <Form.Field>
                  <Checkbox label='I agree to the Terms and Conditions' />
                </Form.Field> */}
                <Button type='submit'>Submit</Button>
              </Form>
              </Card>
            );
        }
        else if(formType===2){
            return (
                <Card>
                <Header as='h3'>
                Advanced Function 2 Parameter
                </Header>
                <Form className="adv2" onSubmit={this.handelFormSubmit}>
                <Form.Field>
                  <label>Price</label>
                  <input name = 'param3' placeholder='Price' />
                </Form.Field>

                <Button type='submit'>Submit</Button>
              </Form>
              </Card>
            );
        }

    }

    handelFormSubmit(event,data){
        const funcType = data.className;
        let reqURL="";

        this.setState({
            errorState: 0,
        });

        if(funcType==="adv1"){
            const postObj = {
                param1: event.target.elements.param1.value,
                param2: event.target.elements.param2.value,
            }
            reqURL = `http://127.0.0.1:8000/maker/${postObj.param1}-${postObj.param2}/adv1`;
            axios.get(reqURL).then((res)=>{
                console.log(res.data);
                this.setState({
                    adv1Data: res.data,
                });
            })
        }
        else if(funcType==="adv2"){
            reqURL = `http://127.0.0.1:8000/maker/${event.target.elements.param3.value}/adv2`;
            axios.get(reqURL).then((res)=>{
                console.log(res.data);
                this.setState({
                    adv2Data: res.data,
                });
            })
        }
 
        
    }
    render(){
        

        return (
            <div className = 'adv-container'>

                {/* {this.detailCard()}<br /> */}
                {this.giveForm(1)}<br />

                {this.advCard(1)}<br/>
                {this.giveForm(2)}<br />

                {this.advCard(2)}<br/><br/>
                <Link to ="../">
                <Button className = "tbb">
                    To Homepage
                </Button>
                </Link>
            </div>
            
        );
    }
}

export default Adv;