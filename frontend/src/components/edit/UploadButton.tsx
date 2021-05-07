import React, { useEffect, useRef, useState } from "react";
import { Form, Button } from "react-bootstrap";
import axios from "axios";
import { useAppSelector, useAppDispatch } from "../../state/hooks";
import { updateUploaded } from "../../state/userSlice";

// TODO move logic into UserEdit component, child components shouldn't be responsible of logic+api calls
const UploadButton = () => {
  const username = useAppSelector((state) => state.user.username);
  const dispatch = useAppDispatch();
  const uploadRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<[File]>();
  const triggerUpload = (e: React.FormEvent) => {
    e.preventDefault();
    // check below here because of typescript error of object is possibly null
    if (uploadRef.current !== null) {
      uploadRef.current.click();
    }
  };

  // todo change to async and await
  useEffect(() => {
    if (files) {
      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
      }
      formData.set("username", username);
      axios({
        method: "POST",
        url: `/api/upload`,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
        .then(() => {
          dispatch(updateUploaded(true));
        })
        .catch((err) => {
          dispatch(updateUploaded(false));
          console.log(err);
        });
    }
  }, [files]);

  const onFileChange = (e: React.FormEvent) => {
    // @ts-ignore
    setFiles([...e.target.files]);
  };

  return (
    <Form onSubmit={triggerUpload} className="mr-auto" inline>
      <Form.File ref={uploadRef} onChange={onFileChange} hidden multiple />
      <Button variant="outline-success" type="submit">
        Upload
      </Button>
    </Form>
  );
};

export default UploadButton;
