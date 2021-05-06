import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import ImageGallery from "../ImageGallery";
import NavigationBar from "./NavigationBarHome";

interface Props {
  username: "";
}

const UserHome = (props: Props) => {
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

export default UserHome;
