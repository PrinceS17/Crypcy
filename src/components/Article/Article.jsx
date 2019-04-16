
import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import 'antd/dist/antd.css';
import { List, Avatar, Icon, Table, Button, Divider, Tag } from 'antd';
import MainTable from "../Tables/MainTable.jsx"

const IconText = ({ type, text }) => (
    <span>
      <Icon type={type} style={{ marginRight: 8 }} />
      {text}
    </span>
  );

  const columns = [{
    title: 'Logo',
    dataIndex: 'logo',
    key: 'logo',
    render: logo => <Avatar size="small" src = {logo} /> ,
  },
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
    render: nameText => <a href="javascript:;">{nameText}</a>,
  }, ];

  
class Article extends Component{
    constructor(props){
        super(props);
    }

    render(){
        console.log(this.props.data);
        return (
            // <Table columns={columns} dataSource={this.props.data} />
            <MainTable data={this.props.data}/>
        //     <List
        //     itemLayout="vertical"
        //     size="large"
        //     pagination={{
        //       onChange: (page) => {
        //         console.log(page);
        //       },
        //       pageSize: 20,
        //     }}
        //     dataSource={this.props.data}//Data Source
        //     // footer={<div><b>ant design</b> footer part</div>}
        //     renderItem={item => (
        //       <List.Item
        //         key={item.id}
        //         // actions={[<IconText type="star-o" text="156" />, <IconText type="like-o" text="156" />, <IconText type="message" text="2" />]}
        //         // extra={<img width={272} alt="logo" src="https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png" />}
        //       >
        //         <List.Item.Meta
        //           avatar={<Avatar src={item.logo} />}
        //           title={<a href={`${this.props.detailURL}${item.id}`}>{item.name}</a>}
        //         //   description={item.description}
        //         />
        //         {item.content}
        //       </List.Item>
        //     )}
        //   />
        );
    }
}

export default Article;