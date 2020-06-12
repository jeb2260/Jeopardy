import React, {Component} from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import './App.css';
import About from './components/About.js';
import Contact from './components/Contact.js';
import NotFound from './components/NotFound.js';
import Glossary from './components/Glossary.js';
import Legal from './components/Legal.js';
import Connect from './components/Connect.js';
import Search from './components/Search.js';
import Footer from './components/Footer.js';

class App extends Component {
  constructor(){
    super()
    console.log("Hello")
  }
  render() {
    return (
      <Router>
        <div className="App">
          <header className="App-header">
            <Switch>
              <Route exact path="/" component={Search} />
              <Route path="/about" component={About}/>
              <Route path="/contact" component={Contact}/>
              <Route path="/legal" component={Legal}/>
              <Route path="/glossary" component={Glossary}/>
              <Route path="/connect" component={Connect}/>
              <Route path="*" component={NotFound}/>
            </Switch>
          </header>
          <Footer />
        </div>
      </Router>
    )
  }
}

export default App;
