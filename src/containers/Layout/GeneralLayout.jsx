import React, { Component } from 'react'
import { Button } from 'semantic-ui-react'
import { Link, withRouter } from 'react-router-dom'
import {Layout, Menu, Dropdown, Breadcrumb, Icon, Table, Divider, Tag} from 'antd';
// import Article from "../../components/Article/Article"
import CrypcyLogo from "../../Assets/Images/CrypcyLogo.png"
import style from "./GeneralLayout.scss"
import {connect} from 'react-redux'
import * as actions from '../../store/actions/auth'
import axios from 'axios';
import SearchBar from "../../components/SearchBar/SearchBar"


const { SubMenu } = Menu;

const {Header, Content, Footer, Sider} = Layout;



class GeneralLayout extends Component{
  constructor(props){
    super(props);
    this.state={
      cCollection: null,
      nCollection: null,
      source: null,
    }
  }

  componentDidMount(){
    const tempURL = `http://34.216.221.19:8000/maker/basic/filter`;
    axios.get(tempURL).then(res => {
      const cRaw = res.data;
      let cS = {};
      cS['name'] = "Cryptocurrency";
      let cR = [];
      for(let c of cRaw){
        let newC = {}
        newC['title'] = c.name;
        newC['image'] = c.logo || '';
        newC['price'] = `$${c.price}` || '';
        newC['link'] = `/currency/${c.crypto_currency_id}`
        cR.push(newC);
      }
      cS['results'] = cR;
      console.log(cS);

      //TODO: Get News

      //Concat Currs and News
      let source = {};
      source['Cryptocurrency'] = cS;
      source['News'] = {'name': 'News', 'results': []}
      this.setState({
        source: source,
      });
    });
  }

  handleLogout = (e) => {
    this.props.logout();
    this.props.history.push(this.props.location.pathname);
  }
  handleLogin = (e) => {
    this.props.history.push('/login');
  }
  render(){
    const menuLoggedIn = (
      <Menu>
        <Menu.Item key="profile"><Link to="/account">Account</Link></Menu.Item>
        {/* <Menu.Item key="setting"><Link to="/user/setting">Setting</Link></Menu.Item> */}
        <Menu.Item key="logout" onClick={this.handleLogout}>Log out</Menu.Item>
      </Menu>
    );

    const menuText = (
        this.props.isAuthenticated ? this.props.loguser : <p></p>
        // <div style={{ lineHeight: '64px', float: 'right', color: 'white', margin: "0 20px"}}>Welcome! {this.props.loguser}</div> 
        // :
        // <div style={{ lineHeight: '64px', float: 'right', color: 'white', margin: "0 20px"}}></div>
      
    );

    let sideMenu = '';
    if(this.props.isAuthenticated){
      sideMenu = (
        <div>
          <Sider width={300}  style={{ background: '#fff', top: '60px'}}>
          <Menu

            mode="inline"
            defaultSelectedKeys={['1']}
            style={{ position: 'fixed', width:'300px' }}
          >
            <Menu.Item key="logout" onClick={this.handleLogout} style={{color:'red'}}><Icon type="logout" />Log out</Menu.Item>
            <Menu.Item key="list"><Link to='/list'><Icon type="dollar" theme="twoTone"/> Cryptocurrency List</Link></Menu.Item>
            <Menu.Item key="profile"><Icon type="smile" theme="twoTone" twoToneColor="#00bb00"/> Profile</Menu.Item>

            <SubMenu key="fav" title={<span><Icon type="star"  theme="twoTone" twoToneColor="#daa520"/>Favorites</span>}>
              <Menu.Item key="5">option5</Menu.Item>
              <Menu.Item key="6">option6</Menu.Item>
              <Menu.Item key="7">option7</Menu.Item>
              <Menu.Item key="8">option8</Menu.Item>
            </SubMenu>
            <SubMenu key="recomm" title={<span><Icon type="like" theme="twoTone" twoToneColor="#eb2f96" />Recommendations</span>}>
              <Menu.Item key="9">option9</Menu.Item>
              <Menu.Item key="10">option10</Menu.Item>
              <Menu.Item key="11">option11</Menu.Item>
              <Menu.Item key="12">option12</Menu.Item>
            </SubMenu>
          </Menu>
        </Sider>
        </div>
      );
    }
    else{
      sideMenu = (
        <div>
        <Sider   width={300}  style={{ background: '#fff', top: '60px'}}>
        <Menu

          mode="inline"
          defaultSelectedKeys={['1']}
          style={{ position: 'fixed', width:'300px' }}
        >
          <Menu.Item key="login"  onClick={this.handleLogin} style={{color:'blue'}}> <Icon type="login" />Log in</Menu.Item>
          <Menu.Item key="list"><Link to='/list'><Icon type="dollar" theme="twoTone"/> Cryptocurrency List</Link></Menu.Item>
        </Menu>
      </Sider>
      </div>
      )
    }
      return (
          <Layout style={{backgroundColor:'#FFF'}}>

            {sideMenu}


            <Header className="header" style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
            
            

              <Link to="/">
              <img src = {CrypcyLogo} style={{height: '64px', top: '-8px', position:'relative'}}/>
              </Link>
              <div className = "SearchBar">
              <SearchBar  source={this.state.source}/>
              </div>


              <Menu
                theme="dark"
                mode="horizontal"
                defaultSelectedKeys={['2']}
                style={{ lineHeight: '64px', float: 'right'}}
              >
{/* 
            
              {
                this.props.isAuthenticated ?

                <Menu.Item key="2">
                  <Dropdown overlay={menuLoggedIn}>
                    <a className="ant-dropdown-link" href="#">
                      {menuText} <Icon type="down" />
                    </a>
                  </Dropdown>
                </Menu.Item>  

                :

                <Menu.Item key="2">
                    <Link to="/login">Login</Link>
                </Menu.Item>
            } */}
              </Menu>
              
              {/* {menuText} */}

            </Header>

            {/* <Content style={{ padding: '0 50px'}} className = 'Content-Header'>
                Cryptocurrency List
            </Content> */}
            <Content  style={{ padding: '0 5px', marginTop: 64 }}>
              {/* <Breadcrumb style={{ margin: '16px 0' }}>
                <Breadcrumb.Item>Home</Breadcrumb.Item>
                <Breadcrumb.Item>List</Breadcrumb.Item>
                <Breadcrumb.Item>App</Breadcrumb.Item>
              </Breadcrumb> */}
              <Layout style={{ padding: '48px 0', background: '#FFF' }}>
                <Content style={{ padding: '0 24px', minHeight: 1000 }}>
                  {this.props.children}
                </Content>
              </Layout>
            </Content>
              
                
              
            
            <Footer style={{ textAlign: 'center', position: 'fixed', bottom: '0', width: '100%', height: '36px' , padding: '5px'}}>
              Design ©2018 Powered By TEAM 42
            </Footer>
        </Layout>
      )
  }
}

const mapStateToProps = (state) => {
  return {
      loguser: state.loguser
  }
}


const mapDispatchToProps = dispatch => {
  return {
      logout: () => {
        dispatch(actions.logout());
      }
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(GeneralLayout));