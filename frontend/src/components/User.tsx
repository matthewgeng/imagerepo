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
  updateTriggerImageLoad,
  selectFiles,
  updateFiles,
} from "../state/userSlice";
import { getFiles } from "../api/filesApi";
interface Params {
  username: "";
}

// const IMAGES = [
//   {
//     src: "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_b.jpg",
//     thumbnail:
//       "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_n.jpg",
//     thumbnailWidth: 320,
//     thumbnailHeight: 174,
//   },
//   {
//     src: "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_b.jpg",
//     thumbnail:
//       "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_n.jpg",
//     thumbnailWidth: 320,
//     thumbnailHeight: 212,
//   },

//   {
//     src: "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_b.jpg",
//     thumbnail:
//       "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_n.jpg",
//     thumbnailWidth: 320,
//     thumbnailHeight: 212,
//   },
// ];

interface RecievedFile {
  _id: string;
  filename: string;
  src: string;
  metadata: Object;
  thumbnail: boolean;
  uploadDate: string;
}

const User = () => {
  const params: Params = useParams();
  const dispatch = useAppDispatch();
  const triggerImageLoad = useAppSelector(selectTriggerImageLoad);
  dispatch(updateUsername(params.username));

  // loading data
  useEffect(() => {
    // not my preferred trigger method maybe better?
    if (triggerImageLoad) {
      const getFilesAsync = async (username: string) => {
        const rawData = await getFiles(username);
        const parsed: Object[] = [];
        const objectArr: Object[] = Object.values(rawData.data);
        for (const f of objectArr) {
          // @ts-ignore
          delete f._id;
          // @ts-ignore
          delete f.filename;
          // @ts-ignore
          delete f.height;
          // @ts-ignore
          delete f.width;
          // @ts-ignore
          delete f.thumb_id;
          // @ts-ignore
          delete f.uploadDate;
          // // @ts-ignore
          // delete f.thumbnailWidth;
          // // @ts-ignore
          // delete f.thumbnailHeight;
          parsed.push(f);
        }
        dispatch(updateFiles(parsed));
        console.log(parsed);
        dispatch(updateTriggerImageLoad(false));
      };
      getFilesAsync(params.username);
    }
  }, [triggerImageLoad]);
  const images = useAppSelector(selectFiles);
  const newArray = images.map((item) => {
    // { ...item } creates a new object and spreads all of "item" items
    // into it. We can then assign a "newField" or overwrite "newField"
    // if it already exists on "item"
    return { ...item };
  });
  return (
    <Router>
      <Switch>
        <Route exact path="/:username">
          <UserHome images={newArray} />
        </Route>
        <Route exact path="/:username/edit">
          <UserEdit images={newArray} />
        </Route>
        <Route path="*">
          <NoMatch />
        </Route>
      </Switch>
    </Router>
  );
};

export default User;
