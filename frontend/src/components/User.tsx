import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  useParams,
} from "react-router-dom";
import NoMatch from "./NoMatch";
import UserHome from "./home/UserHome";
import UserEdit from "./edit/UserEdit";

interface Params {
  username: "";
}

const User = () => {
  const params: Params = useParams();

  return (
    <Router>
      <Switch>
        <Route exact path="/:username">
          <UserHome username={params.username} />
        </Route>
        <Route exact path="/:username/edit">
          <UserEdit username={params.username} />
        </Route>
        <Route path="*">
          <NoMatch />
        </Route>
      </Switch>
    </Router>
  );
};

export default User;
