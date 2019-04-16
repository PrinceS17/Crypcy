import React, { Component } from 'react';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import 'semantic-ui-css/semantic.min.css';
import 'antd/dist/antd.css'; 
import {connect} from 'react-redux'
import * as actions from "../../Store/actions/auth"

import './App.css';
import Home from "../Home/home.jsx";
import ListView from "../ListView/listView.jsx";
import DetailView from "../DetailView/detailView.jsx";
import Adv from "../Advanced/adv.jsx"
import Signin from "../Auth/signin.jsx"

class App extends Component {
  // componentDidMount(){
  //   this.props.onTryAutoSignup();
  // }

  render() {
    return (
      <Router basename={process.env.PUBLIC_URL}>
        <Switch>
          <Route exact path = "/" component={Home} />
          <Route path = "/login" component={Signin} />
          <Route path = "/list" component = {ListView} /> 
          <Route path="/detail/:ix"  render={(props) => (<DetailView key={props.match.params.ix} {...props} />) }/>
          <Route path = "/adv" component = {Adv} />
        </Switch>
      </Router>
    );
  }
}

export default App;
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
