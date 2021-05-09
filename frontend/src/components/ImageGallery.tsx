import React from "react";
import Gallery from "react-grid-gallery";

interface Props {
  images: Object[];
}

const ImageGallery = (props: Props) => {
  // return <ReactPhotoGallery photos={photos} />;
  return <Gallery images={props.images} />;
};

export default ImageGallery;
