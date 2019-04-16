import { Table, Button } from 'antd';
import React from 'react';


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

  clearFilters = () => {
    this.setState({ filteredInfo: null });
  }

  clearAll = () => {
    this.setState({
      filteredInfo: null,
      sortedInfo: null,
    });
  }

  setAgeSort = () => {
    this.setState({
      sortedInfo: {
        order: 'descend',
        columnKey: 'age',
      },
    });
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
      //   filters: [
      //     { text: 'Joe', value: 'Joe' },
      //     { text: 'Jim', value: 'Jim' },
      //   ],
      },
        {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    //   filters: [
    //     { text: 'Joe', value: 'Joe' },
    //     { text: 'Jim', value: 'Jim' },
    //   ],
    //   filteredValue: filteredInfo.name || null,
    //   onFilter: (value, record) => record.name.includes(value),
      sorter: (a, b) => (a.name<b.name?-1:(a.name>b.name?1:0)),
      sortOrder: sortedInfo.columnKey === 'name' && sortedInfo.order,
    }, {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
      sorter: (a, b) => a.age - b.age,
      sortOrder: sortedInfo.columnKey === 'age' && sortedInfo.order,
    }, {
      title: 'Address',
      dataIndex: 'address',
      key: 'address',
    //   filters: [
    //     { text: 'London', value: 'London' },
    //     { text: 'New York', value: 'New York' },
    //   ],
    //   filteredValue: filteredInfo.address || null,
    //   onFilter: (value, record) => record.address.includes(value),
      sorter: (a, b) => a.address.length - b.address.length,
      sortOrder: sortedInfo.columnKey === 'address' && sortedInfo.order,
    }];
    return (
      <div>
        <div className="table-operations">
          <Button onClick={this.setAgeSort}>Sort age</Button>
          <Button onClick={this.clearFilters}>Clear filters</Button>
          <Button onClick={this.clearAll}>Clear filters and sorters</Button>
        </div>
        <Table columns={columns} dataSource={this.props.data} onChange={this.handleChange} pagination={{defaultPageSize: 120}}/>
      </div>
    );
  }
}

export default MainTable