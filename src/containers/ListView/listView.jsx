import React, { Component } from 'react'
import { InputNumber, Button, Card, Spin } from 'antd';
import {Form} from 'semantic-ui-react'

import axios from 'axios'
import styles from './listView.css'
import MainTable from "../../components/Tables/MainTable"
import { relativeTimeRounding } from 'moment';


//Backend Filtering??

class ListView extends Component{
    constructor(props){
        super(props);
        this.state = {
            collection: [],
            errorState: 0,
            priceLow: 0,
            priceHigh: 100000,
            utilLow: 0,
            utilHigh: 100000,
            isloading: false,
        };
        this.fetchList = this.fetchList.bind(this);
        this.clearAllFilter = this.clearAllFilter.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange= this.handleChange.bind(this);
    }

    componentDidMount(){
        this.fetchList();
        document.title = "Cryptocurrency List";
    }

    fetchList(){
        const tempURL = `http://34.216.221.19:8000/maker/basic/filter?price1=${this.state.priceLow}&price2=${this.state.priceHigh}&utility1=${this.state.utilLow}&utility2=${this.state.utilHigh}`;
        this.setState({
            isloading: true
        })
        console.log(tempURL);
        axios.get(tempURL).then(res=>{
            this.setState({
                collection: res.data,
                isloading: false,
            });
            
        })
    }

    clearAllFilter(){
        this.setState({
            priceLow: 0,
            priceHigh: 100000,
            utilLow: 0,
            utilHigh: 100000,
        });
        this.fetchList();

    }

    handleSubmit = ()=>{
        this.fetchList();
    }

    handleChange = (e, { name, value }) => this.setState({ [name]: value });

    render(){
        let errorMessage = this.state.errorState===1? "Input Unvalid":"";
        if(this.state.errorState===2)  errorMessage="Insert Successful";
        return(
            <div style={{position: "relative"}}>
                <div  className = "CardContainer">
                    <Card
                    className="Card"
                    title="Top Cryptocurrencies List"
                    bordered={false}
                    >

                    <Form onSubmit={this.handleSubmit} className="Form">
                        <Form.Group>
                        <Form.Input placeholder='Price From' name='priceLow' onChange={this.handleChange} style={{ margin: "0px 40px 0x 40px"}} />
                        <Form.Input placeholder='To' name='priceHigh'  onChange={this.handleChange} style={{ margin: "0px 40px 0x 40px"}} />

                        <Form.Input placeholder='Utility From' name='utilLow'  onChange={this.handleChange} style={{ margin: "0px 40px 0x 40px"}}/>

                        <Form.Input placeholder='To' name='utilHigh' onChange={this.handleChange} style={{ margin: "0px 40px 0x 40px"}}/>
                        <Form.Button type='primary' content='Filter' />
                        <Form.Button secondary content='Clear'  onClick={this.clearAllFilter}/>
                        </Form.Group>
                    </Form>

{/* 
                    <Form.Group inline widths='equal' className = "FormGroup" >
                        Price from
                        <input placeholder='Low Price' name="lp" onChange={this.filterChange} style={{margin: "8px"}}/>
                        to
                        <input placeholder='High Price' name='hp' onChange={this.filterChange} style={{ margin: "8px 36px 8px 8px"}}/>

                        Utility from
                        <input placeholder='Low Utility' name='lu' onChange={this.filterChange} style={{margin: "8px 8px 8px 8px"}}/>
                        to
                        <input  placeholder='High Utility' name='hu' onChange={this.filterChange} style={{ margin: "8px"}}/>
                        <Button type="primary" style={{margin:'0 8px'} } onClick={this.handleSubmit}> Filter </Button>
                        <Button type="danger" style={{margin:'0 8px'}} onClick={this.clearAllFilter}> Clear </Button>
                    </Form.Group> */}
                    

                    </Card>

                </div>
                 


                {
                    (this.state.collection && this.state.collection.length>0 && this.state.isloading===false)?
                    
                    <MainTable data = {this.state.collection} detailURL = '../detail/' />
                    :
                    <Spin size="large" tip="Fetching Data" className="Spin"/>
                    
                }

                 
            </div>
            
        );
    }
}

export default ListView;