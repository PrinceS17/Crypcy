import { Table, Button } from 'antd';
import React from 'react';
import {withRouter} from 'react-router-dom';

class MainTable extends React.Component {
  state = {
    filteredInfo: null,
    sortedInfo: null,
  };

  handleChange = (pagination, filters, sorter) => {
    console.log('Various parameters', pagination, filters, sorter);
    this.setState({
      filteredInfo: filters,
      sortedInfo: sorter,
    });
  }


  routeChange(path) {
    console.log(path);
    this.props.history.push(path);
  }

  render() {

    let { sortedInfo, filteredInfo } = this.state;
    sortedInfo = sortedInfo || {};
    filteredInfo = filteredInfo || {};
    const columns = [{
        dataIndex: ['logo'],
        key: 'logo',
        width: 24,
        render: logo => <img src={logo} style={{height: "28px"}}/>
      },
      {
        title: 'Symbol',
        dataIndex: 'symbol',
        key: 'symbol',
        sorter: (a, b) => (a.symbol<b.symbol?-1:(a.symbol>b.symbol?1:0)),
        sortOrder: sortedInfo.columnKey === 'symbol' && sortedInfo.order,
      },
        {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a, b) => (a.name<b.name?-1:(a.name>b.name?1:0)),
      sortOrder: sortedInfo.columnKey === 'name' && sortedInfo.order,
    }, {
      title: 'Price',
      dataIndex: 'price',
      key: 'price',
      sorter: (a, b) => a.price - b.price,
      sortOrder: sortedInfo.columnKey === 'price' && sortedInfo.order,
    }, {
      title: 'Supply',
      dataIndex: 'supply',
      key: 'supply',
      sorter: (a, b) => a.supply - b.supply,
      sortOrder: sortedInfo.columnKey === 'supply' && sortedInfo.order,
    }, {
      title: 'Utility',
      dataIndex: 'utility',
      key: 'utility',
      sorter: (a, b) => a.utility - b.utility,
      sortOrder: sortedInfo.columnKey === 'utility' && sortedInfo.order,
    }, {
      title: 'Privacy',
      dataIndex: 'privacy',
      key: 'privacy',
      sorter: (a, b) => a.privacy - b.privacy,
      sortOrder: sortedInfo.columnKey === 'privacy' && sortedInfo.order,
    }];



    return (
      <div>
        <div className="table-operations">
          {/* <Button onClick={this.setAgeSort}>Sort age</Button>
          <Button onClick={this.clearFilters}>Clear filters</Button>
          <Button onClick={this.clearAll}>Clear filters and sorters</Button> */}
        </div>
        <Table rowKey="name"  columns={columns} dataSource={this.props.data} onChange={this.handleChange} pagination={{defaultPageSize: 50}}
              onRow={(record,index)=>{
                return {
                  onClick: (event)=>{
                    this.routeChange(`/currency/${record.crypto_currency_id}/`)
                  }
              }}}/>
      </div>
    );
  }
}

export default withRouter(MainTable)