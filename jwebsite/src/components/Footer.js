import React,{Component} from "react"
import bottom from "../images/Footer.png"
import twitter from "../images/Twitter.png"
import '../App.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";


class Footer extends Component{
    render(){
        return (
            <footer >
                <img className = "bottom" responsive="true" src={bottom}/>
                <Link to="/about" className = "category1" style={{ textDecoration: 'none' }}>ABOUT</Link>
                <Link to="/contact" className = "category2" style={{ textDecoration: 'none' }}>CONTACT</Link>
                <Link to="/legal" className = "category3" style={{ textDecoration: 'none' }}>LEGAL</Link>
                <Link to="/glossary" className = "category4" style={{ textDecoration: 'none' }}>GLOSSARY</Link> 
                <a href="http://www.jeopardy.com" className = "category5" style={{ textDecoration: 'none' }}>JEOPARDY!</a>
                <a href="https://twitter.com" className = "category6" style={{ textDecoration: 'none' }}>
                    TWITTER <br/><img src={twitter} alt = "twitter" className="twitterIcon" />
                </a>
            </footer>
        );
    }
}

export default Footer