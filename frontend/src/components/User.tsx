import React, { useEffect } from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  useParams,
} from "react-router-dom";
import NoMatch from "./NoMatch";
import UserHome from "./home/UserHome";
import UserEdit from "./edit/UserEdit";

import { useAppDispatch, useAppSelector } from "../state/hooks";
import {
  updateUsername,
  selectTriggerImageLoad,
  updateFiles,
} from "../state/userSlice";
import { getFiles } from "../api/filesApi";
interface Params {
  username: "";
}

const IMAGES = [
  {
    src: "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_b.jpg",
    thumbnail:
      "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_n.jpg",
    thumbnailWidth: 320,
    thumbnailHeight: 174,
  },
  {
    src: "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_b.jpg",
    thumbnail:
      "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_n.jpg",
    thumbnailWidth: 320,
    thumbnailHeight: 212,
  },

  {
    src: "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_b.jpg",
    thumbnail:
      "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_n.jpg",
    thumbnailWidth: 320,
    thumbnailHeight: 212,
  },
];

const User = () => {
  const params: Params = useParams();
  const dispatch = useAppDispatch();
  const triggerImageLoad = useAppSelector(selectTriggerImageLoad);
  dispatch(updateUsername(params.username));

  // loading data
  useEffect(() => {
    const getFilesAsync = async (username: string) => {
      const data = await getFiles(username);
      dispatch(updateFiles(data.data));
      console.log(data);
    };
    getFilesAsync(params.username);
  }, [triggerImageLoad]);

  return (
    <Router>
      <Switch>
        <Route exact path="/:username">
          <UserHome images={IMAGES} />
        </Route>
        <Route exact path="/:username/edit">
          <UserEdit images={IMAGES} />
        </Route>
        <Route path="*">
          <NoMatch />
        </Route>
      </Switch>
    </Router>
  );
};

export default User;
