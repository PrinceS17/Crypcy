import React, { Component } from 'react'
import { Button } from 'antd'
import { Link } from 'react-router-dom'
import styles from './welcome.scss'
import { Carousel, Card, Row, Col, Icon, Avatar } from 'antd';
import Logo from '../../Assets/Images/CrypcyLogo.png'

function importAll(r) {
    return r.keys().map(r);
  }

const images = importAll(require.context('../../Assets/Crypcy_pic', false, /\.(png|jpe?g|svg)$/));
const team = importAll(require.context('../../Assets/Team', false, /\.(png|jpe?g|svg)$/));

const { Meta } = Card;

const IconFont = Icon.createFromIconfontCN({
    scriptUrl: '//at.alicdn.com/t/font_8d5l8fzk5b87iudi.js',
  });


class Welcome extends Component{
    componentDidMount(){
        document.title = "Welcome to Crypcy";
    }
    render(){
        return (
            <div className = "Home" style={{textAlign:'center', position: 'relative'}}>

                <div className="Carsl" style={{width: '70%', textAlign:'center'}}>
                    <div className="Home-header">
                    <h1 className="Info-text-h1">Welcome to Crypcy</h1>
                    <h3 className="Info-text-h3"> A Smart Cryptocurrency Info Site</h3>
                    <Link to="/list">
                    <Button type="primary" style={{position: "relative", top: "40px"}}>
                        Get Started
                    </Button>  
                    </Link>
                    </div>
                    
                    <Carousel dots autoplay effect="scrollx">
                        <img className="Carsl-Img" src={images[5]}/>
                        <img className="Carsl-Img" src={images[2]}/>
                        <img className="Carsl-Img" src={images[6]}/>
                        

                    </Carousel>
                </div>
                <br/>
                <Icon size='large' type="arrow-down" />        More Info       <Icon type="arrow-down" className="Icons"/>

                <h1 className="WTD">What Can We Do?</h1>
                <Row type="flex" justify="space-between">
                <Col span={5}>
                <Card
                    hoverable
                    cover={<img className="Modal-Img" alt="example" src={images[4]} />}
                >
                    <Meta
                    title="Cryptocurrency Info"
                    description="Search and view real-time data of hundres of cryptocurrencies"
                    />
                </Card>
                </Col>


                <Col span={5}>
                <Card
                    hoverable
                    cover={<img className="Modal-Img" alt="example" src={images[1]} />}
                >
                    <Meta
                    title="Favorites"
                    description="Manage your list of favorite cryptocurrencies."
                    />
                </Card>
                </Col>

                <Col span={5}>
                <Card
                    hoverable
                    cover={<img className="Modal-Img" alt="example" src={images[8]} />}
                >
                    <Meta
                    title="Recommendation"
                    description="For cryptocurrencies matching your favorites and risk preference"
                    />
                </Card>
                </Col>

                <Col span={5}>
                <Card
                    hoverable
                    cover={<img className="Modal-Img" alt="example" src={images[7]} />}
                >
                    <Meta
                    title="Price Prediction"
                    description="Precise prediction for the next 5 days based on history data"
                    />
                </Card>
                </Col>
                
                </Row>
                <br/>

                <h1 className="WTD">Our Team</h1>
                <Row type="flex" justify="space-around">
                <Col span={11}>
                <Card
                    actions={[<a href="https://www.linkedin.com/in/fhzeng/"><Icon type="linkedin" /></a>,<a href="https://github.com/zengfh"><Icon type="github" /></a>]}
                >
                    <Meta
                    avatar={<Avatar size="large" src={team[0]} />}
                    title="Hank Zeng"
                    description="Frontend Development"
                    />
                </Card>
                </Col>
                <Col span={11}>
                <Card
                    actions={[<a href="https://www.linkedin.com/in/jinhui-song/"><Icon type="linkedin" /></a>,<a href="https://github.com/PrinceS17/"><Icon type="github" /></a>]}
                >
                    <Meta
                    avatar={<Avatar size="large" src={`https://media.licdn.com/dms/image/C4E03AQHV4vTuXaPyzg/profile-displayphoto-shrink_800_800/0?e=1561593600&v=beta&t=NYfg5nopAJBf_GFAf-MDxZeQJVchid0iMqvs6qWmavk`} />}
                    title="Jinhui Song"
                    description="Backend Development / Algorithm Design"
                    />
                </Card>
                </Col>
                </Row>

                <br /><br />
                <Row type="flex" justify="space-around">
                <Col span={11}>
                <Card
                    actions={[<a href="https://www.linkedin.com/in/ruixin-zou-79365715b/"><Icon type="linkedin" /></a>,<a href="https://github.com/ZRX97"><Icon type="github" /></a>]}
                >
                    <Meta
                    avatar={<Avatar size="large" src={team[1]} />}
                    title="Ruixin Zou"
                    description="Backend Development"
                    />
                </Card>
                </Col>
                <Col span={11}>
                <Card
                    actions={[<a href="https://www.linkedin.com/in/yichi-zhang-555346157/"><Icon  type="linkedin" /></a>,<a href="https://github-dev.cs.illinois.edu/yichiz3"><Icon type="github" /></a>]}
                >
                    <Meta
                    avatar={<Avatar size="large" src={team[2]} />}
                    title="Yichi Zhang"
                    description="Algorithm Design"
                    />
                </Card>
                </Col>
                </Row>
            </div>
        )
    }
}

export default Welcome;