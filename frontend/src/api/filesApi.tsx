import axios from "axios";

export const uploadFiles = (files: File[], username: string) => {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append("files", files[i]);
  }
  formData.set("username", username);
  return axios({
    method: "POST",
    url: `/api/upload`,
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  })
    .then((res) => res)
    .catch((err) => {
      console.error(err);
      throw err;
    });
};
