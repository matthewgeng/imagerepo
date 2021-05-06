import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import ImageGallery from "../ImageGallery";
import NavigationBar from "./NavigationBarEdit";

interface Props {
  username: "";
}

const UserEdit = (props: Props) => {
  return (
    <Container fluid>
      <NavigationBar username={props.username} />
      <Row>
        <Col>
          <ImageGallery />
        </Col>
      </Row>
    </Container>
  );
};

export default UserEdit;
