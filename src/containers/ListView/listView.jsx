import React, { Component } from 'react'
import { InputNumber, Button, Card, Spin } from 'antd';
import {Form} from 'semantic-ui-react'
import {connect} from 'react-redux'

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
            filtered: false,
        };
        this.fetchList = this.fetchList.bind(this);
        this.clearAllFilter = this.clearAllFilter.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange= this.handleChange.bind(this);
    }

    componentDidMount(){
        // this.fetchList();
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
            filtered: false,
        });
        this.fetchList();

    }

    handleSubmit = ()=>{
        this.fetchList();
        this.setState({
            filtered: true,
        })
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


                    </Card>

                </div>
                 


                {
                    // (this.props.CurrencyList && this.props.CurrencyList.length>0)?
                    (this.state.filtered && this.state.collection.length > 0)?
                    <MainTable data = {this.state.collection} detailURL = '../detail/' />
                    :
                    <MainTable data = {this.props.CurrencyList} detailURL = '../detail/' />
                }

                 
            </div>
            
        );
    }
}



const mapStateToProps = (state) => {
    return {
        CurrencyList: state.CurrencyList,
    }
  }

export default connect(mapStateToProps, null)(ListView);
