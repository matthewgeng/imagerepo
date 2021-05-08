import React, { useRef, useState } from "react";
import { Form, Button } from "react-bootstrap";
import { useAppSelector, useAppDispatch } from "../../state/hooks";
import { updateIsUploading, updateUploaded } from "../../state/userSlice";
import { uploadFiles } from "../../api/filesApi";

// TODO move logic into UserEdit component, child components shouldn't be responsible of logic+api calls
const UploadButton = () => {
  const username = useAppSelector((state) => state.user.username);
  const dispatch = useAppDispatch();
  const uploadRef = useRef<HTMLInputElement>(null);
  const triggerUpload = (e: React.FormEvent) => {
    e.preventDefault();
    // check below here because of typescript error of object is possibly null
    if (uploadRef.current !== null) {
      uploadRef.current.click();
    }
  };

  // const uploadFiles = (formData: FormData) => {
  //   axios({
  //     method: "POST",
  //     url: `/api/upload`,
  //     data: formData,
  //     headers: {
  //       "Content-Type": "multipart/form-data",
  //     },
  //   })
  //     .then(() => {
  //       dispatch(updateUploaded(true));
  //     })
  //     .catch((err) => {
  //       dispatch(updateUploaded(false));
  //       console.error(err);
  //     });
  // };

  const onFileInput = async (e: React.FormEvent) => {
    dispatch(updateIsUploading(true));
    dispatch(updateUploaded(false));
    // this below is needed for typescript otherwise it would be clean  const files: File[] = [...e.target.files];
    const target = e.target as HTMLInputElement;
    const files: File[] = [...Array.from(target.files as FileList)];

    await uploadFiles(files, username);
    dispatch(updateIsUploading(false));
    dispatch(updateUploaded(true));
  };

  const resetFileInput = (e: React.FormEvent) => {
    // @ts-ignore
    e.target.value = null;
  };

  return (
    <Form onSubmit={triggerUpload} className="mr-auto" inline>
      <Form.File
        ref={uploadRef}
        onInput={onFileInput}
        onClick={resetFileInput}
        hidden
        multiple
      />
      <Button variant="outline-success" type="submit">
        Upload
      </Button>
    </Form>
  );
};

export default UploadButton;
