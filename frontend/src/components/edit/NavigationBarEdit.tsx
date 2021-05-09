import React from "react";
import { Navbar, Form, FormControl, Button } from "react-bootstrap";

import { Link } from "react-router-dom";
import UploadButton from "./UploadButton";
import { useAppSelector } from "../../state/hooks";
import { downloadFiles } from "../../api/filesApi";

const NavigationBar = () => {
  const username = useAppSelector((state) => state.user.username);
  const url = "/" + username;

  const downloadUserFiles = async (e: React.FormEvent) => {
    e.preventDefault();
    await downloadFiles(username);
  };
  return (
    <Navbar bg="light" expand="lg" sticky="top">
      <Navbar.Brand>
        <Link to={url} className="navbar-brand">
          {username}
        </Link>
      </Navbar.Brand>
      <UploadButton />
      <Form onSubmit={downloadUserFiles} className="mr-auto" inline>
        <Button variant="outline-primary" type="submit">
          Download All
        </Button>
      </Form>
      <Form inline>
        <FormControl type="text" placeholder="Search" className="mr-sm-2" />
        <Button variant="outline-success">Search</Button>
      </Form>
    </Navbar>
  );
};

export default NavigationBar;
