import React, { Component } from 'react';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import 'semantic-ui-css/semantic.min.css';
import 'antd/dist/antd.css'; 
import {connect} from 'react-redux';
import * as actions from "../../store/actions/auth";

import './App.css'

import Login from "../../containers/Login"
import Signup from "../../containers/Signup"
import Profile from "../../containers/Profile"

import Welcome from "../Welcome/welcome.jsx";
import GeneralLayout from '../../containers/Layout/GeneralLayout';

import ListView from "../../containers/ListView/listView.jsx";
import DetailView from "../../containers/DetailView/detailView.jsx";






class App extends Component {
  componentDidMount(){
    this.props.onTryAutoSignup();
  }

  render() {
    return (
      <Router basename={process.env.PUBLIC_URL}>
      <GeneralLayout {...this.props}>
        <Switch>
            <Route exact path = "/" component={Welcome} />
            <Route path = "/login" component={Login} />
            <Route path = "/signup" component={Signup} />
            <Route path = "/profile/:ix" render={(props) => (<Profile key={props.match.params.ix} {...props} /> )}/>
            <Route path = "/list" component = {ListView} /> 
            <Route path="/currency/:ix"  render={(props) => (<DetailView key={props.match.params.ix} {...props} />) }/>
        </Switch>
      </GeneralLayout>

      </Router>
    );
  }
}

// export default App;
const mapStateToProps = state =>{
  return {
    isAuthenticated: state.token !== null
  } 
}

const mapDispatchToProps = dispatch =>{
  return {
    onTryAutoSignup: () => dispatch(actions.authCheckState())
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(App);
