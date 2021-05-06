import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import ImageGallery from "../ImageGallery";
import NavigationBar from "./NavigationBarHome";

const UserHome = () => {
  return (
    <Container fluid>
      <NavigationBar />
      <Row>
        <Col>
          <ImageGallery />
        </Col>
      </Row>
    </Container>
  );
};

export default UserHome;
