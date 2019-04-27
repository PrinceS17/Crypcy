import React, { Component } from 'react'
import axios from "axios";
import {Spin, Card, Icon, Menu, Button, Form, Radio, Col, Row, notification, Dropdown } from 'antd';
import {withRouter} from 'react-router-dom'
import styles from './detailView.css'
import Areanull from "../../components/Charts/Areanull.jsx"
import { string } from 'prop-types';
import {connect} from 'react-redux'
import * as actions from '../../store/actions/auth'

const { Meta } = Card;


class DetailView extends Component{
    constructor(props){
        super(props);
        this.state={
            metrics: null,
            predicted: null,
            schema: "",
            outData: [],

        }
        this.fetchMetrics = this.fetchMetrics.bind(this);
        this.setPlotData = this.setPlotData.bind(this);
    }

    fetchMetrics(){
        const detailID = this.props.match.params.ix;
        
        const metricURL = `http://34.216.221.19:8000/maker/basic/detail?id=${detailID}`;
        axios.get(metricURL)
        .then((res)=>{
            let resData = res.data;
            const preData = resData.shift();
            this.setState({
                metrics: resData,
                predicted: preData['prediction'],
                 
            });
            if(!this.state.schema) this.setPlotData("price");
            document.title = "Detail | " + res.data[1].name;
            console.log(preData);
        }).catch((err)=>{
            console.log(err);
        });

    }
    componentDidMount(){
        this.fetchMetrics();
        var detailFetchInterval = setInterval(this.fetchMetrics, 300000);
        this.setState({intervalId: detailFetchInterval});
        var detailFetchInterval = setInterval(this.fetchMetrics, 300000);
        this.setState({intervalId: detailFetchInterval});
        
    }
    componentWillUnmount(){
        clearInterval(this.state.intervalId);
    }
    setPlotData(type='price'){
        if(type===this.state.schema) return;
        if(!this.state.metrics) return;
        let outdata = [];
        outdata = this.state.metrics.map((metric, idx)=>{
            let newmtr = {};
            let timeslot = parseInt(metric.time, 10) * 1000;
            let a = new Date(timeslot);
            var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            var year = a.getFullYear();
            var month = months[a.getMonth()];
            var date = a.getDate();
            var time = date + ' ' + month + ' ' + year;

            newmtr['time'] = time;
            newmtr[type] = metric[type];
            if(idx==0) newmtr['Price Prediction'] = metric[type];
            return newmtr;
            
        });
        let currData = outdata[0];
        
        outdata = outdata.reverse();
        this.setState({
            schema: type,
            outData: outdata
        });
        
        if(type==='price'){
            let currData1 = {};
            currData1['time'] = currData['time'];
            currData1['Price Precition'] = currData['price'];
            // outdata.push(currData1);
            const currTime = this.state.metrics[0].time;
            for(let i=0;i<5;i++){
                let newmtr = {};
            
                let timeslot = parseInt(currTime, 10) * 1000 + 1000*24*3600 * (i+1);
                console.log(timeslot);
                console.log(timeslot);
                let a = new Date(timeslot);
                var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                var year = a.getFullYear();
                var month = months[a.getMonth()];
                var date = a.getDate();
                var time = date + ' ' + month + ' ' + year;
                newmtr['time'] = time;
                newmtr['Price Prediction'] = this.state.predicted[i];
                outdata.push(newmtr);                
            }
            this.setState({
                outData: outdata,
            });
        }
    }




    
    render(){
        const preMenu =  (
            <Menu>
              <Menu.Item>
                Learning-based prediction for next 5 days' price.
              </Menu.Item>
            </Menu>
          );
          const utilMenu =  (
            <Menu>
              <Menu.Item>
                Utility modeled by price, volume, future response rate, privacy, etc.
              </Menu.Item>
            </Menu>
          );
        
        let details = (
        this.state.metrics? 
            <div className="Details"> 
                <span><h1><img src={this.state.metrics[0].logo}/>    {this.state.metrics[0].name}</h1> </span>
                <span style={{margin: 30}}><h2>{`(${this.state.metrics[0].symbol})`}</h2></span>
                <div style={{ padding: '30px' }}>
                <Row gutter={16} type="flex" style={{textAlign:'center'}} justify="center">
                <Col span={8}>
                    <Card title="Price ($)" bordered={false} ><h3>{this.state.metrics[0].price}</h3></Card>
                </Col>
                <Col span={8}>
                    <Card title="Volume ($)" bordered={false}><h3>{this.state.metrics[0].volume}</h3></Card>
                </Col>
                </Row>
                <br />
                <Row gutter={16} type="flex" style={{textAlign:'center'}} justify="center">
                <Col span={8}>
                    <Card title="Privacy" bordered={false}><h3>{this.state.metrics[0].privacy}</h3></Card>
                </Col>
                <Col span={8}>
                    <Card title={<span>Utility <Dropdown overlay={utilMenu}>
                    <a className="ant-dropdown-link" href="#">   <Icon type="question" />
                    </a>
                </Dropdown></span>} bordered={false}><h3>{this.state.metrics[0].utility}</h3></Card>
                </Col>

                </Row>


            </div>
            
            </div>
            :
            <div></div>
        )
        

        
        let favFlag = 0;
        if(this.props.fav){
            console.log(this.pro)
            let a = this.props.match.params.ix;
            let b = this.props.fav;

            if(b.indexOf(parseInt(a))>-1) favFlag=1;
        }

        let butArea = "";

          
        if(this.props.loguser){
            butArea = (
                favFlag?
                    <Button onClick={()=>{
                        let oldFavs = this.props.fav;
                        let idx = oldFavs.indexOf(parseInt(this.props.match.params.ix));
                        oldFavs.splice(idx,1);
                        let retObj = {}
                        retObj['favorite'] = oldFavs;
                        this.props.updateFavs(this.props.loguser, retObj);
                        notification['success']({
                            message: 'Unfavorite Successful',
                            description: 'The recommendation list will be updated soon on the side bar.',
                          });
                          
                    }} type="danger">Unfavorite</Button>
                    :
                    <Button onClick={()=>{
                        let oldFavs = this.props.fav;
                        oldFavs.push(parseInt(this.props.match.params.ix));
                        let retObj = {}
                        retObj['favorite'] = oldFavs;
                        this.props.updateFavs(this.props.loguser, retObj);
                        notification['success']({
                            message: 'Favorite Successful',
                            description: 'The recommendation list will be updated soon on the side bar.',
                          });
                    }} type="primary">Favorite</Button>
            );
        }
        if(!this.state.metrics){
            return (
              <Spin style={{position:'absolute', left: '50%', top: '50%'}} tip="Loading..." sty></Spin>
            );
          }

        return (
            <div>
                {butArea}
                <br/>
                {details} 
                <br/>

                <div className="Descriptions container">
                <p style={{fontSize: '24px'}}>About</p>
                    {
                        this.state.metrics?
                        this.state.metrics[0].description
                        :
                        <p></p>
                    }
                    
                </div>
                <div className="Graphs  container"  style={{position:'relative', top: '100px'}}>
                <span style={{fontSize: '24px'}}>Performance And Prediction  
                </span>
                    <span> <Dropdown overlay={preMenu}>
                    <a className="ant-dropdown-link" href="#">  What's this <Icon type="question" />
                    </a>
                </Dropdown></span>
                <div> <br /></div>
                <Form className="Form1" style={{position:"absolute", left:"50%"}}>
                <Form.Item
                    >
                   <Radio.Group>
                   <Radio.Button onClick={()=>this.setPlotData("price")}>Price</Radio.Button>
                   <Radio.Button onClick={()=>this.setPlotData("volume")}>Volume</Radio.Button>
                   </Radio.Group>                    
                </Form.Item>
                </Form>
                <Areanull schema={this.state.schema} data={this.state.outData}/>
                </div>

                <br/>
                

            </div>
        )
    }

}

const mapStateToProps = (state) => {
    return {
        fav: state.fav,
        loguser:  state.loguser,
    }
  }
  
  
  const mapDispatchToProps = dispatch => {
    return {
        updateFavs: (username, updates) =>{
            dispatch(actions.updateProfile(username, updates))
        }
    }
  }

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(DetailView));