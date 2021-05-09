import React from "react";
import { Navbar, Nav, Form, FormControl, Button } from "react-bootstrap";

import { Link } from "react-router-dom";

import { useAppSelector } from "../../state/hooks";
const NavigationBar = () => {
  const username = useAppSelector((state) => state.user.username);
  const url = "/" + username;

  return (
    <Navbar bg="light" expand="lg" sticky="top">
      <Navbar.Brand>
        <Link to={url} className="navbar-brand">
          {username}
        </Link>
      </Navbar.Brand>
      <Navbar.Toggle />
      <Navbar.Collapse>
        <Nav className="mr-auto">
          <Link to={url + "/edit"} className="nav-link">
            Edit
          </Link>
        </Nav>
        <Form inline>
          <FormControl type="text" placeholder="Search" className="mr-sm-2" />
          <Button variant="outline-success">Search</Button>
        </Form>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavigationBar;
