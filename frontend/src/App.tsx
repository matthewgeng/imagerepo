import React from "react";
import "./App.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { Container, Jumbotron } from "react-bootstrap";

import User from "./components/User";
import NoMatch from "./components/NoMatch";

const Home = () => (
  <Container className="pt-4 text-center">
    <Jumbotron className="pb-5">
      <h1 className="pb-4">Home</h1>
      <h3>
        go to <code>/username</code>
      </h3>
    </Jumbotron>
  </Container>
);

const App: React.FC = () => (
  <Router>
    <Switch>
      <Route exact path="/">
        <Home />
      </Route>
      <Route path="/:username">
        <User />
      </Route>
      <Route path="*">
        <NoMatch />
      </Route>
    </Switch>
  </Router>
);
export default App;
