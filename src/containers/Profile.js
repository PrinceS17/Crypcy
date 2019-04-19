import React from 'react';
import { Form, Input, Icon, Button, Radio, Alert } from 'antd';
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
    };
  }

  componentDidMount(){
    console.log(this.props);
    axios.get(`http://34.216.221.19:8000/profile/${this.props.match.params.ix}`)
    .then((res)=>{
      this.setState({
          userProfile: res.data,
          loginUser: this.props.match.params.ix,
      })
    });
}

 
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
        // this.props.history.push('/');
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

    return (
        <div style={{position:'relative'}}>
        <div style={{position: 'absolute', left: '50%', width: '50%', transform: "translate(-50%, 0)"}}>

            <div>
                {errorMessage}
                <Form onSubmit={this.handleSubmit} style={{width: "480px"}}>
                <h1 style={{borderBottom: '2px solid'}}>User Profile</h1>
                <Form.Item
                label="Username"
                >
                <span className="ant-form-text">{this.props.loguser}</span>
                </Form.Item>

                <Form.Item
                label="Gender"
                >
                <span className="ant-form-text">{this.state.userProfile.gender}</span>
                </Form.Item>


                <Form.Item
                label="Email"
                >
                <span className="ant-form-text">{this.state.userProfile.email}</span>
                </Form.Item>
              


                <h1 style={{borderBottom: '2px solid'}}>Update Profile</h1>
                <Form.Item label="Gender">
                    {getFieldDecorator('gender')(
                        <Radio.Group>
                        <Radio value="male">Male</Radio>
                        <Radio value="female">Female</Radio>
                        </Radio.Group>
                    )}
                </Form.Item>
                <FormItem>
                {getFieldDecorator('email', {
                    rules: [{
                    type: 'email', message: 'The input is not valid E-mail!',
                    }, {
                    required: true, message: 'Please input your E-mail!',
                    }],
                })(
                    <Input prefix={<Icon type="mail" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="Email" />
                )}
                </FormItem>

                <FormItem>
                {getFieldDecorator('password', {
                    rules: [{
                    required: true, message: 'Please input your password!',
                    }, {
                    validator: this.validateToNextPassword,
                    }],
                })(
                    <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Password" />
                )}
                </FormItem>

                <FormItem>
                {getFieldDecorator('confirm', {
                    rules: [{
                    required: true, message: 'Please confirm your password!',
                    }, {
                    validator: this.compareToFirstPassword,
                    }],
                })(
                    <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="Confirm Password" onBlur={this.handleConfirmBlur} />
                )}
                </FormItem>
                <Form.Item
        >

        </Form.Item>

                <Form.Item label="Interest-tag"> 
                {getFieldDecorator('interest')(
                <Radio.Group>
                <Radio.Button value="Low">Low</Radio.Button>
                <Radio.Button value="Moderate">Moderate</Radio.Button>
                <Radio.Button value="High">High</Radio.Button>
                </Radio.Group>
                )}
                    
                </Form.Item>

                <FormItem>
                <Button type="primary" htmlType="submit" style={{marginRight: '10px'}}>
                    Submit
                </Button>


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
        loguser: state.loguser
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

        
        clearError: ()=>dispatch(actions.clearError())

    }
}

export default connect(mapStateToProps, mapDispatchToProps)(WrappedProfileForm);
