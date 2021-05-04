import React from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  useLocation,
  Switch,
  Route,
} from "react-router-dom";
// boostrap imports, better than importing with wildcard
import Container from "react-bootstrap/Container";
import Jumbotron from "react-bootstrap/Jumbotron";
import SurveyPage from "./components/SurveyPage";

const Home = () => (
  <Container className="pt-4 text-center">
    <Jumbotron className="pb-5">
      <h1 className="pb-4">Home</h1>
      <h3>
        go to <code>/survey/yoursurveyname</code>
      </h3>
      <h3>
        for example: <code>/survey/riskassessment</code>
      </h3>
    </Jumbotron>
  </Container>
);
const NoMatch = () => {
  const location = useLocation();

  return (
    <div>
      <h3>
        No match for <code>{location.pathname}</code>
      </h3>
    </div>
  );
};

const App: React.FC = () => (
  <Router>
    <Switch>
      <Route exact path="/">
        <Home />
      </Route>
      <Route path="/survey/:id">
        <SurveyPage />
      </Route>
      <Route path="*">
        <NoMatch />
      </Route>
    </Switch>
  </Router>
);
export default App;
