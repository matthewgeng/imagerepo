import React, { useRef } from "react";
import { Navbar, Form, FormControl, Button } from "react-bootstrap";

import { Link } from "react-router-dom";
import UploadButton from "./UploadButton";
interface Props {
  username: "";
}

const upload = () => {};

const NavigationBar = (props: Props) => {
  const uploadRef = useRef<HTMLInputElement>(null);
  const url = "/" + props.username;
  return (
    <Navbar bg="light" expand="lg" sticky="top">
      <Navbar.Brand>
        <Link to={url} className="navbar-brand">
          {props.username}
        </Link>
      </Navbar.Brand>
      <UploadButton />
      <Form inline>
        <FormControl type="text" placeholder="Search" className="mr-sm-2" />
        <Button variant="outline-success">Search</Button>
      </Form>
    </Navbar>
  );
};

export default NavigationBar;
