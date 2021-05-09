import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import ImageGallery from "../ImageGallery";
import NavigationBar from "./NavigationBarEdit";

interface Props {
  images: Object[];
}

const UserEdit = (props: Props) => {
  return (
    <Container fluid>
      <NavigationBar />
      <Row>
        <Col>
          <ImageGallery images={props.images} />
        </Col>
      </Row>
    </Container>
  );
};

export default UserEdit;
