import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import ImageGallery from "../ImageGallery";
import NavigationBar from "./NavigationBarEdit";

const UserEdit = () => {
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

export default UserEdit;
