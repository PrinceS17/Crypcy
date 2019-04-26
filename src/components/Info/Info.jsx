import _ from 'lodash'
import React, { Component } from 'react'
import { browserHistory } from 'react-router'

import {withRouter, Redirect} from 'react-router-dom';


class Info extends Component {
  constructor(props){
    super(props);
  }

  render() {
    const { isLoading, value, results } = this.state

    return (
     <div>
        <Alert key='1'
         message={<div>{`Signup Successful! ${this.props.loguser}`} <br /><a href="/list/">Back to Homepage</a></div>} 
         type={this.props.type} showIcon />

     </div>
    )
  }
}

export default Info