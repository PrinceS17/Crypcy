import React, { Component } from 'react'
import axios from "axios";
import { Card, Icon, Avatar, Button, Form, Radio, Col, Row } from 'antd';
import {Link, NavLink} from 'react-router-dom'
import styles from './detailView.css'
import Areanull from "../../components/Charts/Areanull.jsx"
import { string } from 'prop-types';

const { Meta } = Card;


class DetailView extends Component{
    constructor(props){
        super(props);
        this.state={
            metrics: null,
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
            this.setState({
                metrics: res.data
            });
            if(!this.state.schema) this.setPlotData("price");
            document.title = "Detail | " + res.data[0].name;
            console.log(res.data);
        }).catch((err)=>{
            console.log(err);
        });

    }
    componentDidMount(){
        this.fetchMetrics();
        var detailFetchInterval = setInterval(this.fetchMetrics, 100000);
        this.setState({intervalId: detailFetchInterval});
        var detailFetchInterval = setInterval(this.fetchMetrics, 100000);
        this.setState({intervalId: detailFetchInterval});
        
    }

    setPlotData(type='price'){
        if(type===this.state.schema) return;
        if(!this.state.metrics) return;
        let outdata = [];
        outdata = this.state.metrics.map((metric, idx)=>{
            let newmtr = {};
            const timeslot = parseInt(metric.time, 10) * 1000;
            const a = new Date(timeslot);
            var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            var year = a.getFullYear();
            var month = months[a.getMonth()];
            var date = a.getDate();
            var hour = a.getHours();
            var min = a.getMinutes();
            var sec = a.getSeconds();
            var time = date + ' ' + month + ' ' + year;

            newmtr['time'] = time;
            newmtr[type] = metric[type];
            return newmtr;
        });
        outdata = outdata.reverse();
        this.setState({
            schema: type,
            outData: outdata
        });
    }


    componentWillUnmount(){
        clearInterval(this.state.intervalId);
    }

    
    render(){
        const gridStyle = {
            width: '50%',
            textAlign: 'center',
          };
        let details = (
        this.state.metrics? 
            <div className="Details"> 
                <span><h1><img src={this.state.metrics[0].logo}/>    {this.state.metrics[0].name}</h1> </span>

                <div style={{ padding: '30px' }}>
                <Row gutter={16} type="flex" style={{textAlign:'center'}} justify="center">
                <Col span={8}>
                    <Card title="Price" bordered={false} ><h3>{this.state.metrics[0].price}</h3></Card>
                </Col>
                <Col span={8}>
                    <Card title="Volume" bordered={false}><h3>{this.state.metrics[0].volume}</h3></Card>
                </Col>
                </Row>
                <Row gutter={16} type="flex" style={{textAlign:'center'}} justify="center">
                <Col span={8}>
                    <Card title="Utility" bordered={false}><h3>{this.state.metrics[0].utility}</h3></Card>
                </Col>
                <Col span={8}>
                    <Card title="Privacy" bordered={false}><h3>{this.state.metrics[0].privacy}</h3></Card>
                </Col>
                </Row>


            </div>
            
                {/* <Card
                    style={{ width: 300 }}
                    actions={[<Link to ='/'><Icon type="heart" /></Link>]}
                >
                <Meta
                    avatar={<Avatar src={this.state.metrics[0].logo} />}
                    title={this.state.metrics[0].name}
                    description={`Privacy: ${this.state.metrics[0].privacy}`}
                />
                </Card> */}

            </div>
            :
            <div></div>
        )
        


        return (
            <div>
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
                <p style={{fontSize: '24px'}}>Performance Graphs</p>
                <Form className="Form1" style={{position:"absolute", left:"50%"}}>
                <Form.Item
                    >
                   <Radio.Group>
                   <Radio.Button onClick={()=>this.setPlotData("price")}>Price</Radio.Button>
                   <Radio.Button onClick={()=>this.setPlotData("volume")}>Volume</Radio.Button>
                   <Radio.Button onClick={()=>this.setPlotData("utility")}>Utility</Radio.Button>
                   </Radio.Group>                    
                </Form.Item>
                </Form>
                <Areanull schema={this.state.schema} data={this.state.outData} />
                </div>

                <br/>
                

            </div>
        )
    }

}

export default DetailView;