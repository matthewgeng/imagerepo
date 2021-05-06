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

import { useAppDispatch } from "../state/hooks";

import { updateUsername } from "../state/userSlice";

interface Params {
  username: "";
}

const User = () => {
  const params: Params = useParams();
  const dispatch = useAppDispatch();
  dispatch(updateUsername(params.username));
  return (
    <Router>
      <Switch>
        <Route exact path="/:username">
          <UserHome />
        </Route>
        <Route exact path="/:username/edit">
          <UserEdit />
        </Route>
        <Route path="*">
          <NoMatch />
        </Route>
      </Switch>
    </Router>
  );
};

export default User;
