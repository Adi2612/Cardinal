import React, {useState, useEffect} from 'react';
import axios from 'axios'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

import './App.css';
import Home from "./Home";

const App = () => {

  return (
    <Router>
      <div>
        <Switch>
          <Route exact path="/app">
            <Home />
          </Route>
          <Route path="/app/inference">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );



}

export default App;
