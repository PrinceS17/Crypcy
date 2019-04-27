import React from 'react';
import { Form, Input, Icon, Button, Radio, notification, Modal } from 'antd';
import { connect } from 'react-redux';
import { NavLink, withRouter } from 'react-router-dom';
import * as actions from '../store/actions/auth';
import ErrorCard from '../utilities/ErrorCard';
import axios from 'axios';

const FormItem = Form.Item;

class ProfileForm extends React.Component {
  constructor(props){
    super(props);

    this.state = {
      confirmDirty: false,
      userProfile: '',
      fetchFlag: false,
      loginUser: '',
      visible: false,
    };
  }

  getProfile(){
    axios.get(`http://34.216.221.19:8000/profile/${this.props.match.params.ix}`)
    .then((res)=>{
      this.setState({
          userProfile: res.data,
          loginUser: this.props.match.params.ix,
      })
    });
  }
  componentDidMount(){
    console.log(this.props);
    this.getProfile();
}

showModal = () => {
  this.setState({
    visible: true,
  });
}
handleOk = (e) => {
  console.log(e);
  this.setState({
    visible: false,
  });


  axios.delete(`http://34.216.221.19:8000/profile/${this.props.match.params.ix}/`)
        .then((res)=>{
          console.log("deleted");
          this.props.logout();
          window.location = "/";
        });
    
}

handleCancel = (e) => {
  console.log(e);
  this.setState({
    visible: false,
  });
}





openNotificationWithIcon = (type) => {
  notification[type]({
    message: 'Profile Updated',
    description: 'The recommended cryptocurrencies for you would be updated soon.',
  });
};

  handleSubmit = (e) => {
    e.preventDefault();
    let userr = this.state.loginUser;
    this.props.form.validateFieldsAndScroll((err, values) => {
      if (!err) {
        this.props.onAuth(
            userr,
            values.gender,
            values.email,
            values.password,
            values.confirm,
            values.interest,

        );

        this.props.rcmd(userr);
        this.getProfile();
      }
    });
  }

  handleConfirmBlur = (e) => {
    const value = e.target.value;
    this.setState({ confirmDirty: this.state.confirmDirty || !!value });
  }

  compareToFirstPassword = (rule, value, callback) => {
    const form = this.props.form;
    if (value && value !== form.getFieldValue('password')) {
      callback('Two passwords that you enter is inconsistent!');
    } else {
      callback();
    }
  }

  validateToNextPassword = (rule, value, callback) => {
    const form = this.props.form;
    if (value && this.state.confirmDirty) {
      form.validateFields(['confirm'], { force: true });
    }
    callback();
  }

  
  render() {
    let errorMessage = null;

    if (this.props.error) {
        let errorData = this.props.error.response.data;
        console.log(errorData);
        errorMessage = (
            // <p>{this.props.error.message}</p>
            <div>
                <ErrorCard data = {errorData}/>
            </div>
        );
        
    }

    const { getFieldDecorator } = this.props.form;
    if(!this.props.userProfile){
      return (
        <div></div>
      )
    }
    return (
        <div style={{position:'relative'}}>
        <div style={{position: 'absolute', left: '50%', width: '50%', transform: "translate(-50%, 0)"}}>

            <div>
                {errorMessage}
                <Form onSubmit={this.handleSubmit} style={{width: "480px"}}>
              


                <h1 style={{borderBottom: '2px solid'}}>Update Profile</h1>
                <Form.Item label="Gender">
                    {getFieldDecorator('gender',{
                      initialValue: this.props.userProfile.gender,
                    })(
                        <Radio.Group defaultValue="male">
                        <Radio value="Male">Male</Radio>
                        <Radio value="Female">Female</Radio>
                        </Radio.Group>
                    )}
                </Form.Item>

                <Form.Item>
                {getFieldDecorator('email', {

                    rules: [{
                    type: 'email', message: 'The input is not valid E-mail!',
                    }, 

                  ],
                  
                })(
                    <div>
                      <div>Email:</div>
                      <Input defaultValue={this.props.userProfile.email} prefix={<Icon type="mail" style={{ color: 'rgba(0,0,0,.25)' }} />}  />

                    </div>
                )}
                </Form.Item>

                <FormItem>
                {getFieldDecorator('password', {
                    rules: [
                    //   {
                    // required: true, message: 'Please input your password!',
                    // },
                    {
                    validator: this.validateToNextPassword,
                    }],
                })( 
                    <div>
                      <div>Password</div>
                      <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Password" />
                    </div>
                )}
                </FormItem>

                <FormItem>
                {getFieldDecorator('confirm', {
                    rules: [
                    // {
                    // required: true, message: 'Please confirm your password!',
                    // }, 
                    {
                    validator: this.compareToFirstPassword,
                    }],
                })(
                  <div>
                  <div>confirm Password</div>
                  <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Confirm Password" onBlur={this.handleConfirmBlur} />
                </div>
                )}
                </FormItem>
                <Form.Item
        >

        </Form.Item>

                <Form.Item label="Invest Interest and Risk Tolerance"> 
                {getFieldDecorator('interest',{
                  initialValue: this.props.userProfile.interest_tag,
                })(
                <Radio.Group>
                <Radio.Button  value="Low">Low </Radio.Button>
                <Radio.Button  value="Moderate">Moderate</Radio.Button>
                <Radio.Button  value="High">High</Radio.Button>
                </Radio.Group>
                )}
                    
                </Form.Item>

                <FormItem>
                <Button onClick = {()=>{this.openNotificationWithIcon('success')}} type="primary" htmlType="submit" style={{marginRight: '10px'}}>
                    Submit
                </Button>

                <Button type="danger" onClick={this.showModal}>
                Delete Account
                </Button>
                <Modal
                title="User Delete"
                visible={this.state.visible}
                onOk={this.handleOk}
                onCancel={this.handleCancel}
              >
                <h1>Warning</h1>
                Do you really want to delete your account? This operation is not revocable.
              </Modal>

                </FormItem>

            </Form>

            </div>
           

        </div>
    </div>
    );
  }
}


const WrappedProfileForm = Form.create()(ProfileForm);

const mapStateToProps = (state) => {
    return {
        loading: state.loading,
        error: state.error,
        loguser: state.loguser,
        userProfile: state.Profile,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onAuth: (username, gender, email, password1, password2, interest) => {
          
          dispatch(actions.updateProfile(username, {
            gender: gender,
            email: email,
            password1: password1,
            password2: password2,
            interest_tag: interest
          }));

        },

        logout: () => {
          dispatch(actions.logout());
        },


        getrcmd: (username)=>{
          dispatch(actions.getRcmd(username))
        },
        clearError: ()=>dispatch(actions.clearError())

    }
}

export default connect(mapStateToProps, mapDispatchToProps)(WrappedProfileForm);
